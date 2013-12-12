# $ANTLR 3.2 Sep 23, 2009 12:02:23 Plist.g 2013-12-12 17:09:05

import sys
from antlr3 import *
from antlr3.compat import set, frozenset
         
from collections import OrderedDict



# for convenience in actions
HIDDEN = BaseRecognizer.HIDDEN

# token types
BRACE_OPEN=14
ESC_SEQ=8
WS=6
BRACE_CLOSE=15
WS_CHAR=5
IDENTIFIER=7
DICTIONARY_SEPERATOR=11
ARRAY_SEPERATOR=10
HEX_DIGIT=17
ASSIGNMENT=16
COMMENT=4
EOF=-1
BRACKET_CLOSE=13
STRING=9
BRACKET_OPEN=12

# token names
tokenNames = [
    "<invalid>", "<EOR>", "<DOWN>", "<UP>", 
    "COMMENT", "WS_CHAR", "WS", "IDENTIFIER", "ESC_SEQ", "STRING", "ARRAY_SEPERATOR", 
    "DICTIONARY_SEPERATOR", "BRACKET_OPEN", "BRACKET_CLOSE", "BRACE_OPEN", 
    "BRACE_CLOSE", "ASSIGNMENT", "HEX_DIGIT"
]




class PlistParser(Parser):
    grammarFileName = "Plist.g"
    antlr_version = version_str_to_tuple("3.1 Sep 23, 2009 12:02:23")
    antlr_version_str = "3.1 Sep 23, 2009 12:02:23"
    tokenNames = tokenNames

    def __init__(self, input, state=None, *args, **kwargs):
        if state is None:
            state = RecognizerSharedState()

        super(PlistParser, self).__init__(input, state, *args, **kwargs)






                


        

                      
    def displayRecognitionError(self, tokenNames, exception):
        pass



    # $ANTLR start "plist"
    # Plist.g:87:1: plist returns [value] : (lbl_value= dictionary | lbl_value= array );
    def plist(self, ):

        value = None

        lbl_value = None


        try:
            try:
                # Plist.g:91:5: (lbl_value= dictionary | lbl_value= array )
                alt1 = 2
                LA1_0 = self.input.LA(1)

                if (LA1_0 == BRACE_OPEN) :
                    alt1 = 1
                elif (LA1_0 == BRACKET_OPEN) :
                    alt1 = 2
                else:
                    nvae = NoViableAltException("", 1, 0, self.input)

                    raise nvae

                if alt1 == 1:
                    # Plist.g:91:8: lbl_value= dictionary
                    pass 
                    self._state.following.append(self.FOLLOW_dictionary_in_plist474)
                    lbl_value = self.dictionary()

                    self._state.following.pop()


                elif alt1 == 2:
                    # Plist.g:91:31: lbl_value= array
                    pass 
                    self._state.following.append(self.FOLLOW_array_in_plist480)
                    lbl_value = self.array()

                    self._state.following.pop()


                #action start
                            
                value = lbl_value
                    
                #action end

                        
            except RecognitionException, e:
                raise e
        finally:

            pass
        return value

    # $ANTLR end "plist"


    # $ANTLR start "value"
    # Plist.g:93:1: value returns [value] : (lbl_value= dictionary | lbl_value= array | lbl_value= identifier | lbl_value= string );
    def value(self, ):

        value = None

        lbl_value = None


        try:
            try:
                # Plist.g:97:5: (lbl_value= dictionary | lbl_value= array | lbl_value= identifier | lbl_value= string )
                alt2 = 4
                LA2 = self.input.LA(1)
                if LA2 == BRACE_OPEN:
                    alt2 = 1
                elif LA2 == BRACKET_OPEN:
                    alt2 = 2
                elif LA2 == IDENTIFIER:
                    alt2 = 3
                elif LA2 == STRING:
                    alt2 = 4
                else:
                    nvae = NoViableAltException("", 2, 0, self.input)

                    raise nvae

                if alt2 == 1:
                    # Plist.g:97:8: lbl_value= dictionary
                    pass 
                    self._state.following.append(self.FOLLOW_dictionary_in_value508)
                    lbl_value = self.dictionary()

                    self._state.following.pop()


                elif alt2 == 2:
                    # Plist.g:97:31: lbl_value= array
                    pass 
                    self._state.following.append(self.FOLLOW_array_in_value514)
                    lbl_value = self.array()

                    self._state.following.pop()


                elif alt2 == 3:
                    # Plist.g:97:49: lbl_value= identifier
                    pass 
                    self._state.following.append(self.FOLLOW_identifier_in_value520)
                    lbl_value = self.identifier()

                    self._state.following.pop()


                elif alt2 == 4:
                    # Plist.g:97:72: lbl_value= string
                    pass 
                    self._state.following.append(self.FOLLOW_string_in_value526)
                    lbl_value = self.string()

                    self._state.following.pop()


                #action start
                            
                value = lbl_value
                    
                #action end

                        
            except RecognitionException, e:
                raise e
        finally:

            pass
        return value

    # $ANTLR end "value"


    # $ANTLR start "string"
    # Plist.g:99:1: string returns [value] : lbl_string= STRING ;
    def string(self, ):

        value = None

        lbl_string = None

        try:
            try:
                # Plist.g:103:5: (lbl_string= STRING )
                # Plist.g:103:9: lbl_string= STRING
                pass 
                lbl_string=self.match(self.input, STRING, self.FOLLOW_STRING_in_string555)



                #action start
                            
                value = lbl_string.text[1:-1].decode("string_escape")
                    
                #action end

                        
            except RecognitionException, e:
                raise e
        finally:

            pass
        return value

    # $ANTLR end "string"


    # $ANTLR start "identifier"
    # Plist.g:105:1: identifier returns [value] : lbl_identifier= IDENTIFIER ;
    def identifier(self, ):

        value = None

        lbl_identifier = None

        try:
            try:
                # Plist.g:109:5: (lbl_identifier= IDENTIFIER )
                # Plist.g:109:7: lbl_identifier= IDENTIFIER
                pass 
                lbl_identifier=self.match(self.input, IDENTIFIER, self.FOLLOW_IDENTIFIER_in_identifier586)



                #action start
                            
                value = lbl_identifier.text
                    
                #action end

                        
            except RecognitionException, e:
                raise e
        finally:

            pass
        return value

    # $ANTLR end "identifier"


    # $ANTLR start "array"
    # Plist.g:112:1: array returns [value] : BRACKET_OPEN (lbl_first_value= value ( ARRAY_SEPERATOR lbl_value= value )* )? BRACKET_CLOSE ;
    def array(self, ):

        value = None

        lbl_first_value = None

        lbl_value = None


                   
        value = []
            
        try:
            try:
                # Plist.g:116:5: ( BRACKET_OPEN (lbl_first_value= value ( ARRAY_SEPERATOR lbl_value= value )* )? BRACKET_CLOSE )
                # Plist.g:116:8: BRACKET_OPEN (lbl_first_value= value ( ARRAY_SEPERATOR lbl_value= value )* )? BRACKET_CLOSE
                pass 
                self.match(self.input, BRACKET_OPEN, self.FOLLOW_BRACKET_OPEN_in_array617)
                # Plist.g:116:21: (lbl_first_value= value ( ARRAY_SEPERATOR lbl_value= value )* )?
                alt4 = 2
                LA4_0 = self.input.LA(1)

                if (LA4_0 == IDENTIFIER or LA4_0 == STRING or LA4_0 == BRACKET_OPEN or LA4_0 == BRACE_OPEN) :
                    alt4 = 1
                if alt4 == 1:
                    # Plist.g:116:22: lbl_first_value= value ( ARRAY_SEPERATOR lbl_value= value )*
                    pass 
                    self._state.following.append(self.FOLLOW_value_in_array622)
                    lbl_first_value = self.value()

                    self._state.following.pop()
                    #action start
                    value.append(lbl_first_value)
                    #action end
                    # Plist.g:116:84: ( ARRAY_SEPERATOR lbl_value= value )*
                    while True: #loop3
                        alt3 = 2
                        LA3_0 = self.input.LA(1)

                        if (LA3_0 == ARRAY_SEPERATOR) :
                            alt3 = 1


                        if alt3 == 1:
                            # Plist.g:116:85: ARRAY_SEPERATOR lbl_value= value
                            pass 
                            self.match(self.input, ARRAY_SEPERATOR, self.FOLLOW_ARRAY_SEPERATOR_in_array627)
                            self._state.following.append(self.FOLLOW_value_in_array631)
                            lbl_value = self.value()

                            self._state.following.pop()
                            #action start
                            value.append(lbl_value)
                            #action end


                        else:
                            break #loop3



                self.match(self.input, BRACKET_CLOSE, self.FOLLOW_BRACKET_CLOSE_in_array639)




                        
            except RecognitionException, e:
                raise e
        finally:

            pass
        return value

    # $ANTLR end "array"


    # $ANTLR start "dictionary_key"
    # Plist.g:119:1: dictionary_key returns [value] : (lbl_key= identifier | lbl_key= string ) ;
    def dictionary_key(self, ):

        value = None

        lbl_key = None


        try:
            try:
                # Plist.g:123:2: ( (lbl_key= identifier | lbl_key= string ) )
                # Plist.g:123:6: (lbl_key= identifier | lbl_key= string )
                pass 
                # Plist.g:123:6: (lbl_key= identifier | lbl_key= string )
                alt5 = 2
                LA5_0 = self.input.LA(1)

                if (LA5_0 == IDENTIFIER) :
                    alt5 = 1
                elif (LA5_0 == STRING) :
                    alt5 = 2
                else:
                    nvae = NoViableAltException("", 5, 0, self.input)

                    raise nvae

                if alt5 == 1:
                    # Plist.g:123:7: lbl_key= identifier
                    pass 
                    self._state.following.append(self.FOLLOW_identifier_in_dictionary_key668)
                    lbl_key = self.identifier()

                    self._state.following.pop()


                elif alt5 == 2:
                    # Plist.g:123:28: lbl_key= string
                    pass 
                    self._state.following.append(self.FOLLOW_string_in_dictionary_key674)
                    lbl_key = self.string()

                    self._state.following.pop()






                #action start
                         
                value = lbl_key
                	
                #action end

                        
            except RecognitionException, e:
                raise e
        finally:

            pass
        return value

    # $ANTLR end "dictionary_key"


    # $ANTLR start "dictionary_entry"
    # Plist.g:126:1: dictionary_entry returns [value] : lbl_key= dictionary_key ASSIGNMENT lbl_value= value DICTIONARY_SEPERATOR ;
    def dictionary_entry(self, ):

        value = None

        lbl_key = None

        lbl_value = None


        try:
            try:
                # Plist.g:130:5: (lbl_key= dictionary_key ASSIGNMENT lbl_value= value DICTIONARY_SEPERATOR )
                # Plist.g:130:8: lbl_key= dictionary_key ASSIGNMENT lbl_value= value DICTIONARY_SEPERATOR
                pass 
                self._state.following.append(self.FOLLOW_dictionary_key_in_dictionary_entry705)
                lbl_key = self.dictionary_key()

                self._state.following.pop()
                self.match(self.input, ASSIGNMENT, self.FOLLOW_ASSIGNMENT_in_dictionary_entry707)
                self._state.following.append(self.FOLLOW_value_in_dictionary_entry711)
                lbl_value = self.value()

                self._state.following.pop()
                self.match(self.input, DICTIONARY_SEPERATOR, self.FOLLOW_DICTIONARY_SEPERATOR_in_dictionary_entry713)



                #action start
                            
                value = (lbl_key, lbl_value)
                    
                #action end

                        
            except RecognitionException, e:
                raise e
        finally:

            pass
        return value

    # $ANTLR end "dictionary_entry"


    # $ANTLR start "dictionary"
    # Plist.g:133:1: dictionary returns [value] : BRACE_OPEN (lbl_entry= dictionary_entry )* BRACE_CLOSE ;
    def dictionary(self, ):

        value = None

        lbl_entry = None


                   
        entries = []
            
        try:
            try:
                # Plist.g:140:5: ( BRACE_OPEN (lbl_entry= dictionary_entry )* BRACE_CLOSE )
                # Plist.g:140:8: BRACE_OPEN (lbl_entry= dictionary_entry )* BRACE_CLOSE
                pass 
                self.match(self.input, BRACE_OPEN, self.FOLLOW_BRACE_OPEN_in_dictionary753)
                # Plist.g:140:19: (lbl_entry= dictionary_entry )*
                while True: #loop6
                    alt6 = 2
                    LA6_0 = self.input.LA(1)

                    if (LA6_0 == IDENTIFIER or LA6_0 == STRING) :
                        alt6 = 1


                    if alt6 == 1:
                        # Plist.g:140:20: lbl_entry= dictionary_entry
                        pass 
                        self._state.following.append(self.FOLLOW_dictionary_entry_in_dictionary758)
                        lbl_entry = self.dictionary_entry()

                        self._state.following.pop()
                        #action start
                        entries.append(lbl_entry)
                        #action end


                    else:
                        break #loop6
                self.match(self.input, BRACE_CLOSE, self.FOLLOW_BRACE_CLOSE_in_dictionary764)



                #action start
                            
                value = OrderedDict(entries)
                    
                #action end

                        
            except RecognitionException, e:
                raise e
        finally:

            pass
        return value

    # $ANTLR end "dictionary"


    # Delegated rules


 

    FOLLOW_dictionary_in_plist474 = frozenset([1])
    FOLLOW_array_in_plist480 = frozenset([1])
    FOLLOW_dictionary_in_value508 = frozenset([1])
    FOLLOW_array_in_value514 = frozenset([1])
    FOLLOW_identifier_in_value520 = frozenset([1])
    FOLLOW_string_in_value526 = frozenset([1])
    FOLLOW_STRING_in_string555 = frozenset([1])
    FOLLOW_IDENTIFIER_in_identifier586 = frozenset([1])
    FOLLOW_BRACKET_OPEN_in_array617 = frozenset([7, 9, 12, 13, 14])
    FOLLOW_value_in_array622 = frozenset([10, 13])
    FOLLOW_ARRAY_SEPERATOR_in_array627 = frozenset([7, 9, 12, 14])
    FOLLOW_value_in_array631 = frozenset([10, 13])
    FOLLOW_BRACKET_CLOSE_in_array639 = frozenset([1])
    FOLLOW_identifier_in_dictionary_key668 = frozenset([1])
    FOLLOW_string_in_dictionary_key674 = frozenset([1])
    FOLLOW_dictionary_key_in_dictionary_entry705 = frozenset([16])
    FOLLOW_ASSIGNMENT_in_dictionary_entry707 = frozenset([7, 9, 12, 14])
    FOLLOW_value_in_dictionary_entry711 = frozenset([11])
    FOLLOW_DICTIONARY_SEPERATOR_in_dictionary_entry713 = frozenset([1])
    FOLLOW_BRACE_OPEN_in_dictionary753 = frozenset([7, 9, 12, 14, 15])
    FOLLOW_dictionary_entry_in_dictionary758 = frozenset([7, 9, 12, 14, 15])
    FOLLOW_BRACE_CLOSE_in_dictionary764 = frozenset([1])



def main(argv, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr):
    from antlr3.main import ParserMain
    main = ParserMain("PlistLexer", PlistParser)
    main.stdin = stdin
    main.stdout = stdout
    main.stderr = stderr
    main.execute(argv)


if __name__ == '__main__':
    main(sys.argv)
