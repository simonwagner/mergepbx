grammar Plist;

options 
{
	language=Python;
}

@header {
from collections import OrderedDict

from ..escape import unescape_string
}

@rulecatch {
except RecognitionException, e:
    raise e
}

@lexer::members {
def displayRecognitionError(self, tokenNames, exception):
    pass
}

@parser::members {
def displayRecognitionError(self, tokenNames, exception):
    pass
}

COMMENT
    :   '//' ~('\n'|'\r')* '\r'? '\n' {$channel=HIDDEN;}
    |   '/*' ( options {greedy=false;} : . )* '*/' {$channel=HIDDEN;}
    ;

WS	:	(WS_CHAR) {$channel=HIDDEN;}
	;

IDENTIFIER
    :	(~(';' | WS_CHAR | '=' | '(' | ')' | '{' | '}' | ',' | '"' | '<' | '>' ))+
    ;

STRING
    :  '"' ( ESC_SEQ | ~('\\'|'"') )* '"'
    ;

ARRAY_SEPERATOR
	:	','
	;

DICTIONARY_SEPERATOR
	:	';'
	;

BRACKET_OPEN
	:	'('
	;

BRACKET_CLOSE
	:	')'
	;

BRACE_OPEN
	:	'{'
	;

BRACE_CLOSE
	:	'}'
	;

ASSIGNMENT
        :	'='
        ;
	
fragment
HEX_DIGIT : ('0'..'9'|'a'..'f'|'A'..'F') ;

fragment
ESC_SEQ
    :   '\\' ('b'|'t'|'n'|'f'|'r'|'\"'|'\''|'\\')
    ;
fragment
WS_CHAR  
    :   ( ' '
        | '\t'
        | '\r'
        | '\n'
        ) 
    ;

plist returns [value]
    @after {
        $value = $lbl_value.value
    }
    :  lbl_value=dictionary | lbl_value=array;

value returns [value]
    @after {
    	$value = $lbl_value.value
    }
    :  lbl_value=dictionary | lbl_value=array | lbl_value=identifier | lbl_value=string;

string returns [value]
    @after {
        $value = unescape_string($lbl_string.text[1:-1])
    }
    :   lbl_string=STRING;
    
identifier returns [value]
    @after {
        $value = $lbl_identifier.text
    }
    :	lbl_identifier=IDENTIFIER
    ;

array returns [value]
    @init {
    	$value = []
    }
    :  BRACKET_OPEN (lbl_first_value=value {$value.append($lbl_first_value.value)} (ARRAY_SEPERATOR lbl_value=value {$value.append($lbl_value.value)})*)? (ARRAY_SEPERATOR)? BRACKET_CLOSE
    ;

dictionary_key returns [value]
	@after {
		$value = $lbl_key.value
	}
	:   (lbl_key=identifier | lbl_key=string)
	;

dictionary_entry returns [value]
    @after {
       $value = ($lbl_key.value, $lbl_value.value)
    }
    :  lbl_key=dictionary_key ASSIGNMENT lbl_value=value DICTIONARY_SEPERATOR
    ;

dictionary returns [value]
    @init {
    	entries = []
    }
    @after {
    	$value = OrderedDict(entries)
    }
    :  BRACE_OPEN (lbl_entry=dictionary_entry {entries.append($lbl_entry.value)})* BRACE_CLOSE 
    ;	

