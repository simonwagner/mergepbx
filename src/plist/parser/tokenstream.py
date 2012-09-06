from itertools import chain, islice
import logging

logger = logging.getLogger("plist.parser.tokenstream")

class _lazylist(object):
    def __init__(self, generator):
        self.list = None
        self.generator = generator

    def __repr__(self):
        if self.list == None:
            self.list = list(self.generator)
        return repr(self.list)

class TokenIter(object):
    def __init__(self, iterator, lexer = None):
        self.iterator = iterator
        self.lexer = lexer
        self.buffer = []
        self.logger = logging.getLogger("plist.parser.tokeniter")

    def __iter__(self):
        #first push out everything from buffer
        while len(self.buffer) > 0:
            buffer_item = self.buffer.pop()
            self.logger.debug("yielding %s from buffer", buffer_item.name)
            yield buffer_item

        #read from iterator
        #if there are items in the buffer, yield them first
        #before yielding the next item from iterator
        for item in self.iterator:
            while len(self.buffer) > 0:
                buffer_item = self.buffer.pop()
                self.logger.debug("yielding %s from buffer", buffer_item.name)
                yield buffer_item

            self.logger.debug("yielding %s from stream", item.name)
            yield item

        #no more items in iterator
        #yield the rest of the buffer
        while len(self.buffer) > 0:
            buffer_item = self.buffer.pop()
            self.logger.debug("yielding %s from buffer", buffer_item.name)
            yield buffer_item

        #clear buffer
        self.buffer = None

    def push_tokens(self, tokens):
        self.buffer.extend(tokens)            

    def expect(self, token_name):
        if not self.lexer is None:
            self.lexer.expect(token_name)

class TokenStream(object):
    def __init__(self, lexer, input, ignore_tokens=[]):
        self.ignore_tokens = set(ignore_tokens)
        #self.token_iter = (token for token in lexer.scan(input) if not token.name in self.ignore_tokens)
        token_generator = (token for token in lexer.scan(input) if not token.name in self.ignore_tokens)
        self.token_iter = TokenIter(token_generator, lexer)

    def peek(self, n=1):
        peeked_elements = self._read_tokens(n)
        self.push_tokens(peeked_elements)
        logger.debug("peeked at tokens %r", _lazylist(token.name for token in peeked_elements))
        return peeked_elements

    def pop(self, n=1):
        poped_tokens = self._read_tokens(n)
        logger.debug("poped tokens %r", _lazylist(token.name for token in poped_tokens))
        return poped_tokens

    def push_tokens(self, tokens):
        #self.token_iter = chain(tokens, self.token_iter)
        self.token_iter.push_tokens(tokens)

    def expect(self, token_name):
        self.token_iter.expect(token_name)

    def _read_tokens(self, n):
        return list(islice(self.token_iter, 0, n))

class BacktrackingTokenStream(TokenStream):
    def __init__(self, token_stream):
        global count_backtracking

        self.token_stream = token_stream
        self.token_buffer = None
        self.backtracking = False

    @staticmethod
    def create(token_stream):
        if isinstance(token_stream, BacktrackingTokenStream) and not token_stream.is_dirty():
            return token_stream #reuse non-dirty BacktrackingTokenStream
        else:
            return BacktrackingTokenStream(token_stream)

    def is_dirty(self):
        return self.token_buffer != None

    def backtrack(self):
        logger.debug("enabled backtracking on token stream %d", id(self))
        self.backtracking = True
        assert(self.token_buffer == None or len(self.token_buffer) == 0)

    def pop(self, n=1):
        tokens_read = self.token_stream._read_tokens(n)
        if self.backtracking: 
            self._save_tokens(tokens_read)
            logger.debug("poped tokens %r (bt) on %d", _lazylist(token.name for token in tokens_read), id(self))
            logger.debug("token buffer for %d: %r", id(self), _lazylist(token.name for token in self.token_buffer))
        else:
            logger.debug("poped tokens %r", _lazylist(token.name for token in tokens_read))
        return tokens_read

    def _save_tokens(self, tokens):
        if self.token_buffer == None:
            self.token_buffer = []
        self.token_buffer += tokens

    def fail(self):
        if self.token_buffer != None and len(self.token_buffer) > 0:
            logger.debug("restore tokens %r on %d", _lazylist(token.name for token in self.token_buffer), id(self))
            self.token_stream.push_tokens(self.token_buffer)
            self.token_buffer = None
        else:
           logger.debug("restore tokens: no tokens in buffer") 
        self.backtracking = False

    def success(self):
        logger.debug("succeess, clearing token buffer %d", id(self))
        self.token_buffer = None
        self.backtracking = False

    def push_tokens(self, tokens):
        return self.token_stream.push_tokens(tokens)

    def peek(self, n=1):
        return self.token_stream.peek(n)

    def expect(self, token_name):
        self.token_stream.expect(token_name)

    def _read_tokens(self, n):
        return self.token_stream._read_tokens(n)
