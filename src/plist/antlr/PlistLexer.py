# $ANTLR 3.2 Sep 23, 2009 12:02:23 Plist.g 2013-12-12 18:02:36

import sys
from itertools import chain
from .runtime.antlr3 import *
from .runtime.antlr3.compat import set, frozenset


# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
BRACE_OPEN=13
WS=16
ESC_SEQ=7
BRACE_CLOSE=14
WS_CHAR=5
IDENTIFIER=6
DICTIONARY_SEPERATOR=10
ARRAY_SEPERATOR=9
HEX_DIGIT=17
ASSIGNMENT=15
COMMENT=4
EOF=-1
BRACKET_CLOSE=12
STRING=8
BRACKET_OPEN=11

"""
yield all numbers from start to stop, including start and stop
"""
def range_inc(start, stop):
    current = start
    while current <= stop:
        yield current
        current += 1


class PlistLexer(Lexer):

    grammarFileName = "Plist.g"
    antlr_version = version_str_to_tuple("3.1 Sep 23, 2009 12:02:23")
    antlr_version_str = "3.1 Sep 23, 2009 12:02:23"

    def __init__(self, input=None, state=None):
        if state is None:
            state = RecognizerSharedState()
        super(PlistLexer, self).__init__(input, state)


        self.dfa7 = self.DFA7(
            self, 7,
            eot = self.DFA7_eot,
            eof = self.DFA7_eof,
            min = self.DFA7_min,
            max = self.DFA7_max,
            accept = self.DFA7_accept,
            special = self.DFA7_special,
            transition = self.DFA7_transition
            )




                               
    def displayRecognitionError(self, tokenNames, exception):
        pass



    # $ANTLR start "COMMENT"
    def mCOMMENT(self, ):

        try:
            _type = COMMENT
            _channel = DEFAULT_CHANNEL

            # Plist.g:28:5: ( '//' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' | '/*' ( options {greedy=false; } : . )* '*/' )
            alt4 = 2
            LA4_0 = self.input.LA(1)

            if (LA4_0 == 47) :
                LA4_1 = self.input.LA(2)

                if (LA4_1 == 47) :
                    alt4 = 1
                elif (LA4_1 == 42) :
                    alt4 = 2
                else:
                    nvae = NoViableAltException("", 4, 1, self.input)

                    raise nvae

            else:
                nvae = NoViableAltException("", 4, 0, self.input)

                raise nvae

            if alt4 == 1:
                # Plist.g:28:9: '//' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
                pass 
                self.match("//")
                # Plist.g:28:14: (~ ( '\\n' | '\\r' ) )*
                while True: #loop1
                    alt1 = 2
                    LA1_0 = self.input.LA(1)

                    if ((0 <= LA1_0 <= 9) or (11 <= LA1_0 <= 12) or (14 <= LA1_0 <= 65535)) :
                        alt1 = 1


                    if alt1 == 1:
                        # Plist.g:28:14: ~ ( '\\n' | '\\r' )
                        pass
                        LA1_2 = self.input.LA(1)
                        if (0 <= LA1_2 <= 9) or (11 <= LA1_2 <= 12) or (14 <= LA1_2 <= 65535):
                            self.input.consume()
                        else:
                            mse = MismatchedSetException(None, self.input)
                            self.recover(mse)
                            raise mse



                    else:
                        break #loop1
                # Plist.g:28:28: ( '\\r' )?
                alt2 = 2
                LA2_0 = self.input.LA(1)

                if (LA2_0 == 13) :
                    alt2 = 1
                if alt2 == 1:
                    # Plist.g:28:28: '\\r'
                    pass 
                    self.match(13)



                self.match(10)
                #action start
                _channel=HIDDEN;
                #action end


            elif alt4 == 2:
                # Plist.g:29:9: '/*' ( options {greedy=false; } : . )* '*/'
                pass 
                self.match("/*")
                # Plist.g:29:14: ( options {greedy=false; } : . )*
                while True: #loop3
                    alt3 = 2
                    LA3_0 = self.input.LA(1)

                    if (LA3_0 == 42) :
                        LA3_1 = self.input.LA(2)

                        if (LA3_1 == 47) :
                            alt3 = 2
                        elif ((0 <= LA3_1 <= 46) or (48 <= LA3_1 <= 65535)) :
                            alt3 = 1


                    elif ((0 <= LA3_0 <= 41) or (43 <= LA3_0 <= 65535)) :
                        alt3 = 1


                    if alt3 == 1:
                        # Plist.g:29:42: .
                        pass 
                        self.matchAny()


                    else:
                        break #loop3
                self.match("*/")
                #action start
                _channel=HIDDEN;
                #action end


            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "COMMENT"



    # $ANTLR start "IDENTIFIER"
    IDENTIFIER_SET = frozenset(chain(
                        range_inc(0,8),
                        range_inc(11,12),
                        range_inc(14,31),
                        range_inc(33,33),
                        range_inc(35,39),
                        range_inc(42,43),
                        range_inc(45,58),
                        range_inc(63,122),
                        range_inc(124,124)
                        ))

    def mIDENTIFIER(self, ):

        try:
            _type = IDENTIFIER
            _channel = DEFAULT_CHANNEL

            # Plist.g:33:5: ( (~ ( ';' | WS_CHAR | '=' | '(' | ')' | '{' | '}' | ',' | '\"' | '<' | '>' ) )+ )
            # Plist.g:33:7: (~ ( ';' | WS_CHAR | '=' | '(' | ')' | '{' | '}' | ',' | '\"' | '<' | '>' ) )+
            pass 
            # Plist.g:33:7: (~ ( ';' | WS_CHAR | '=' | '(' | ')' | '{' | '}' | ',' | '\"' | '<' | '>' ) )+
            cnt5 = 0
            while True: #loop5
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if LA5_0 in self.IDENTIFIER_SET or (126 <= LA5_0 <= 65535):
                    alt5 = 1


                if alt5 == 1:
                    # Plist.g:33:8: ~ ( ';' | WS_CHAR | '=' | '(' | ')' | '{' | '}' | ',' | '\"' | '<' | '>' )
                    pass
                    la = self.input.LA(1)
                    if la in self.IDENTIFIER_SET or (126 <= la <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    if cnt5 >= 1:
                        break #loop5

                    eee = EarlyExitException(5, self.input)
                    raise eee

                cnt5 += 1



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "IDENTIFIER"



    # $ANTLR start "STRING"
    def mSTRING(self, ):

        try:
            _type = STRING
            _channel = DEFAULT_CHANNEL

            # Plist.g:37:5: ( '\"' ( ESC_SEQ | ~ ( '\\\\' | '\"' ) )* '\"' )
            # Plist.g:37:8: '\"' ( ESC_SEQ | ~ ( '\\\\' | '\"' ) )* '\"'
            pass 
            self.match(34)
            # Plist.g:37:12: ( ESC_SEQ | ~ ( '\\\\' | '\"' ) )*
            while True: #loop6
                alt6 = 3
                LA6_0 = self.input.LA(1)

                if (LA6_0 == 92) :
                    alt6 = 1
                elif ((0 <= LA6_0 <= 33) or (35 <= LA6_0 <= 91) or (93 <= LA6_0 <= 65535)) :
                    alt6 = 2


                if alt6 == 1:
                    # Plist.g:37:14: ESC_SEQ
                    pass 
                    self.mESC_SEQ()


                elif alt6 == 2:
                    # Plist.g:37:24: ~ ( '\\\\' | '\"' )
                    pass
                    LA6_1 = self.input.LA(1)
                    if (0 <= LA6_1 <= 33) or (35 <= LA6_1 <= 91) or (93 <= LA6_1 <= 65535):
                        self.input.consume()
                    else:
                        mse = MismatchedSetException(None, self.input)
                        self.recover(mse)
                        raise mse



                else:
                    break #loop6
            self.match(34)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "STRING"



    # $ANTLR start "ARRAY_SEPERATOR"
    def mARRAY_SEPERATOR(self, ):

        try:
            _type = ARRAY_SEPERATOR
            _channel = DEFAULT_CHANNEL

            # Plist.g:41:2: ( ',' )
            # Plist.g:41:4: ','
            pass 
            self.match(44)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ARRAY_SEPERATOR"



    # $ANTLR start "DICTIONARY_SEPERATOR"
    def mDICTIONARY_SEPERATOR(self, ):

        try:
            _type = DICTIONARY_SEPERATOR
            _channel = DEFAULT_CHANNEL

            # Plist.g:45:2: ( ';' )
            # Plist.g:45:4: ';'
            pass 
            self.match(59)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "DICTIONARY_SEPERATOR"



    # $ANTLR start "BRACKET_OPEN"
    def mBRACKET_OPEN(self, ):

        try:
            _type = BRACKET_OPEN
            _channel = DEFAULT_CHANNEL

            # Plist.g:49:2: ( '(' )
            # Plist.g:49:4: '('
            pass 
            self.match(40)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "BRACKET_OPEN"



    # $ANTLR start "BRACKET_CLOSE"
    def mBRACKET_CLOSE(self, ):

        try:
            _type = BRACKET_CLOSE
            _channel = DEFAULT_CHANNEL

            # Plist.g:53:2: ( ')' )
            # Plist.g:53:4: ')'
            pass 
            self.match(41)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "BRACKET_CLOSE"



    # $ANTLR start "BRACE_OPEN"
    def mBRACE_OPEN(self, ):

        try:
            _type = BRACE_OPEN
            _channel = DEFAULT_CHANNEL

            # Plist.g:57:2: ( '{' )
            # Plist.g:57:4: '{'
            pass 
            self.match(123)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "BRACE_OPEN"



    # $ANTLR start "BRACE_CLOSE"
    def mBRACE_CLOSE(self, ):

        try:
            _type = BRACE_CLOSE
            _channel = DEFAULT_CHANNEL

            # Plist.g:61:2: ( '}' )
            # Plist.g:61:4: '}'
            pass 
            self.match(125)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "BRACE_CLOSE"



    # $ANTLR start "ASSIGNMENT"
    def mASSIGNMENT(self, ):

        try:
            _type = ASSIGNMENT
            _channel = DEFAULT_CHANNEL

            # Plist.g:65:9: ( '=' )
            # Plist.g:65:11: '='
            pass 
            self.match(61)



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "ASSIGNMENT"



    # $ANTLR start "WS"
    def mWS(self, ):

        try:
            _type = WS
            _channel = DEFAULT_CHANNEL

            # Plist.g:68:4: ( ( WS_CHAR ) )
            # Plist.g:68:6: ( WS_CHAR )
            pass 
            # Plist.g:68:6: ( WS_CHAR )
            # Plist.g:68:7: WS_CHAR
            pass 
            self.mWS_CHAR()



            #action start
            _channel=HIDDEN;
            #action end



            self._state.type = _type
            self._state.channel = _channel

        finally:

            pass

    # $ANTLR end "WS"



    # $ANTLR start "HEX_DIGIT"
    def mHEX_DIGIT(self, ):

        try:
            # Plist.g:72:11: ( ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' ) )
            # Plist.g:72:13: ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' )
            pass
            LA0 = self.input.LA(1)
            if (48 <= LA0 <= 57) or (65 <= LA0 <= 70) or (97 <= LA0 <= 102):
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "HEX_DIGIT"



    # $ANTLR start "ESC_SEQ"
    def mESC_SEQ(self, ):

        try:
            # Plist.g:76:5: ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) )
            # Plist.g:76:9: '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' )
            pass 
            self.match(92)
            LA0 = self.input.LA(1)
            if LA0 == 34 or LA0 == 39 or LA0 == 92 or LA0 == 98 or LA0 == 102 or LA0 == 110 or LA0 == 114 or LA0 == 116:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "ESC_SEQ"



    # $ANTLR start "WS_CHAR"
    def mWS_CHAR(self, ):

        try:
            # Plist.g:80:5: ( ( ' ' | '\\t' | '\\r' | '\\n' ) )
            # Plist.g:80:9: ( ' ' | '\\t' | '\\r' | '\\n' )
            pass
            LA0 = self.input.LA(1)
            if (9 <= LA0 <= 10) or LA0 == 13 or LA0 == 32:
                self.input.consume()
            else:
                mse = MismatchedSetException(None, self.input)
                self.recover(mse)
                raise mse





        finally:

            pass

    # $ANTLR end "WS_CHAR"



    def mTokens(self):
        # Plist.g:1:8: ( COMMENT | IDENTIFIER | STRING | ARRAY_SEPERATOR | DICTIONARY_SEPERATOR | BRACKET_OPEN | BRACKET_CLOSE | BRACE_OPEN | BRACE_CLOSE | ASSIGNMENT | WS )
        alt7 = 11
        alt7 = self.dfa7.predict(self.input)
        if alt7 == 1:
            # Plist.g:1:10: COMMENT
            pass 
            self.mCOMMENT()


        elif alt7 == 2:
            # Plist.g:1:18: IDENTIFIER
            pass 
            self.mIDENTIFIER()


        elif alt7 == 3:
            # Plist.g:1:29: STRING
            pass 
            self.mSTRING()


        elif alt7 == 4:
            # Plist.g:1:36: ARRAY_SEPERATOR
            pass 
            self.mARRAY_SEPERATOR()


        elif alt7 == 5:
            # Plist.g:1:52: DICTIONARY_SEPERATOR
            pass 
            self.mDICTIONARY_SEPERATOR()


        elif alt7 == 6:
            # Plist.g:1:73: BRACKET_OPEN
            pass 
            self.mBRACKET_OPEN()


        elif alt7 == 7:
            # Plist.g:1:86: BRACKET_CLOSE
            pass 
            self.mBRACKET_CLOSE()


        elif alt7 == 8:
            # Plist.g:1:100: BRACE_OPEN
            pass 
            self.mBRACE_OPEN()


        elif alt7 == 9:
            # Plist.g:1:111: BRACE_CLOSE
            pass 
            self.mBRACE_CLOSE()


        elif alt7 == 10:
            # Plist.g:1:123: ASSIGNMENT
            pass 
            self.mASSIGNMENT()


        elif alt7 == 11:
            # Plist.g:1:134: WS
            pass 
            self.mWS()







    # lookup tables for DFA #7

    DFA7_eot = DFA.unpack(
        u"\1\uffff\1\2\12\uffff\3\2\1\uffff\2\2\1\17"
        )

    DFA7_eof = DFA.unpack(
        u"\23\uffff"
        )

    DFA7_min = DFA.unpack(
        u"\1\0\1\52\12\uffff\3\0\1\uffff\3\0"
        )

    DFA7_max = DFA.unpack(
        u"\1\uffff\1\57\12\uffff\3\uffff\1\uffff\3\uffff"
        )

    DFA7_accept = DFA.unpack(
        u"\2\uffff\1\2\1\3\1\4\1\5\1\6\1\7\1\10\1\11\1\12\1\13\3\uffff\1"
        u"\1\3\uffff"
        )

    DFA7_special = DFA.unpack(
        u"\1\5\13\uffff\1\0\1\6\1\1\1\uffff\1\4\1\2\1\3"
        )

            
    DFA7_transition = [
        DFA.unpack(u"\11\2\2\13\2\2\1\13\22\2\1\13\1\2\1\3\5\2\1\6\1\7\2"
        u"\2\1\4\2\2\1\1\13\2\1\5\1\uffff\1\12\1\uffff\74\2\1\10\1\2\1\11"
        u"\uff82\2"),
        DFA.unpack(u"\1\15\4\uffff\1\14"),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u""),
        DFA.unpack(u"\11\16\2\17\2\16\1\17\22\16\1\17\1\16\1\17\5\16\2\17"
        u"\2\16\1\17\16\16\4\17\74\16\1\17\1\16\1\17\uff82\16"),
        DFA.unpack(u"\11\21\2\17\2\21\1\17\22\21\1\17\1\21\1\17\5\21\2\17"
        u"\1\20\1\21\1\17\16\21\4\17\74\21\1\17\1\21\1\17\uff82\21"),
        DFA.unpack(u"\11\16\2\17\2\16\1\17\22\16\1\17\1\16\1\17\5\16\2\17"
        u"\2\16\1\17\16\16\4\17\74\16\1\17\1\16\1\17\uff82\16"),
        DFA.unpack(u""),
        DFA.unpack(u"\11\21\2\17\2\21\1\17\22\21\1\17\1\21\1\17\5\21\2\17"
        u"\1\20\1\21\1\17\2\21\1\22\13\21\4\17\74\21\1\17\1\21\1\17\uff82"
        u"\21"),
        DFA.unpack(u"\11\21\2\17\2\21\1\17\22\21\1\17\1\21\1\17\5\21\2\17"
        u"\1\20\1\21\1\17\16\21\4\17\74\21\1\17\1\21\1\17\uff82\21"),
        DFA.unpack(u"\11\21\2\uffff\2\21\1\uffff\22\21\1\uffff\1\21\1\uffff"
        u"\5\21\2\uffff\1\20\1\21\1\uffff\16\21\4\uffff\74\21\1\uffff\1\21"
        u"\1\uffff\uff82\21")
    ]

    # class definition for DFA #7

    class DFA7(DFA):
        pass

        SET1 = frozenset(chain(
            range_inc(0,8),
            range_inc(11,12),
            range_inc(14,31),
            range_inc(33,33),
            range_inc(35,39),
            range_inc(42,43),
            range_inc(45, 58),
            range_inc(63, 122),
            range_inc(124,124),
        ))
        SET2 = frozenset(chain(
            range_inc(9, 10),
            range_inc(13,13),
            range_inc(32, 32),
            range_inc(34, 34),
            range_inc(40, 41),
            range_inc(44, 44),
            range_inc(59, 62),
            range_inc(123, 123),
            range_inc(125, 125),
        ))
        def specialStateTransition(self_, s, input):
            # convince pylint that my self_ magic is ok ;)
            # pylint: disable-msg=E0213

            # pretend we are a member of the recognizer
            # thus semantic predicates can be evaluated
            self = self_.recognizer

            _s = s

            if s == 0: 
                LA7_12 = input.LA(1)

                s = -1
                if LA7_12 in self_.SET1 or (126 <= LA7_12 <= 65535):
                    s = 14

                elif LA7_12 in self_.SET2:
                    s = 15

                else:
                    s = 2

                if s >= 0:
                    return s
            elif s == 1: 
                LA7_14 = input.LA(1)

                s = -1
                if LA7_14 in self_.SET2:
                    s = 15

                elif LA7_14 in self_.SET1 or (126 <= LA7_14 <= 65535):
                    s = 14

                else:
                    s = 2

                if s >= 0:
                    return s
            elif s == 2: 
                LA7_17 = input.LA(1)

                s = -1
                if (LA7_17 == 42):
                    s = 16

                elif LA7_17 in self_.SET1 or (126 <= LA7_17 <= 65535):
                    s = 17

                elif LA7_17 in self_.SET2:
                    s = 15

                else:
                    s = 2

                if s >= 0:
                    return s
            elif s == 3: 
                LA7_18 = input.LA(1)

                s = -1
                if (LA7_18 == 42):
                    s = 16

                elif LA7_18 in self_.SET1 or (126 <= LA7_18 <= 65535):
                    s = 17

                else:
                    s = 15

                if s >= 0:
                    return s
            elif s == 4: 
                LA7_16 = input.LA(1)

                s = -1
                if (LA7_16 == 47):
                    s = 18

                elif (LA7_16 == 42):
                    s = 16

                elif LA7_16 in self_.SET1 or (126 <= LA7_16 <= 65535):
                    s = 17

                elif LA7_16 in self_.SET2:
                    s = 15

                else:
                    s = 2

                if s >= 0:
                    return s
            elif s == 5: 
                LA7_0 = input.LA(1)

                s = -1
                if (LA7_0 == 47):
                    s = 1

                elif LA7_0 in self_.SET1 or (126 <= LA7_0 <= 65535):
                    s = 2

                elif (LA7_0 == 34):
                    s = 3

                elif (LA7_0 == 44):
                    s = 4

                elif (LA7_0 == 59):
                    s = 5

                elif (LA7_0 == 40):
                    s = 6

                elif (LA7_0 == 41):
                    s = 7

                elif (LA7_0 == 123):
                    s = 8

                elif (LA7_0 == 125):
                    s = 9

                elif (LA7_0 == 61):
                    s = 10

                elif ((9 <= LA7_0 <= 10) or LA7_0 == 13 or LA7_0 == 32):
                    s = 11

                if s >= 0:
                    return s
            elif s == 6: 
                LA7_13 = input.LA(1)

                s = -1
                if (LA7_13 == 42):
                    s = 16

                elif LA7_13 in self_.SET1 or (126 <= LA7_13 <= 65535):
                    s = 17

                elif LA7_13 in self_.SET2:
                    s = 15

                else:
                    s = 2

                if s >= 0:
                    return s

            nvae = NoViableAltException(self_.getDescription(), 7, _s, input)
            self_.error(nvae)
            raise nvae
 



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import LexerMain
    main = LexerMain(PlistLexer)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)
