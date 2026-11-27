# Generated from /workspaces/admin-urban-json/packages/urban-json/grammar/JsltParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,63,357,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,26,7,26,
        2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,32,2,33,
        7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,39,7,39,
        2,40,7,40,1,0,1,0,1,0,1,1,1,1,1,2,1,2,1,2,1,2,5,2,92,8,2,10,2,12,
        2,95,9,2,1,2,1,2,1,2,1,2,3,2,101,8,2,1,3,1,3,1,3,1,3,1,4,1,4,1,5,
        1,5,1,5,1,5,5,5,113,8,5,10,5,12,5,116,9,5,1,5,1,5,1,5,1,5,3,5,122,
        8,5,1,6,1,6,1,6,3,6,127,8,6,1,7,1,7,3,7,131,8,7,1,8,1,8,3,8,135,
        8,8,1,8,3,8,138,8,8,1,9,1,9,3,9,142,8,9,1,10,1,10,3,10,146,8,10,
        1,11,1,11,1,12,1,12,1,13,3,13,153,8,13,1,13,1,13,1,13,1,13,5,13,
        159,8,13,10,13,12,13,162,9,13,1,14,1,14,1,14,1,14,1,14,1,14,1,14,
        3,14,171,8,14,3,14,173,8,14,1,15,1,15,1,15,1,15,1,15,1,15,1,15,1,
        15,3,15,183,8,15,1,16,1,16,1,17,1,17,3,17,189,8,17,1,18,1,18,1,18,
        3,18,194,8,18,1,18,1,18,3,18,198,8,18,1,18,3,18,201,8,18,1,19,1,
        19,1,20,1,20,1,20,5,20,208,8,20,10,20,12,20,211,9,20,1,21,3,21,214,
        8,21,1,21,1,21,3,21,218,8,21,1,22,1,22,3,22,222,8,22,1,23,1,23,3,
        23,226,8,23,1,24,1,24,3,24,230,8,24,1,25,1,25,1,25,3,25,235,8,25,
        1,25,3,25,238,8,25,1,25,1,25,1,25,3,25,243,8,25,1,25,1,25,3,25,247,
        8,25,3,25,249,8,25,1,26,1,26,1,26,1,26,1,27,1,27,1,27,1,27,5,27,
        259,8,27,10,27,12,27,262,9,27,3,27,264,8,27,1,27,1,27,1,28,1,28,
        3,28,270,8,28,1,28,3,28,273,8,28,1,29,1,29,1,30,1,30,1,30,1,30,1,
        30,1,30,1,30,1,30,1,30,1,30,3,30,287,8,30,1,30,3,30,290,8,30,1,30,
        1,30,3,30,294,8,30,3,30,296,8,30,1,31,1,31,1,31,1,31,3,31,302,8,
        31,1,32,1,32,1,33,1,33,1,34,1,34,1,34,1,35,1,35,1,35,1,36,1,36,1,
        36,1,36,1,37,3,37,319,8,37,1,37,1,37,1,37,1,37,4,37,325,8,37,11,
        37,12,37,326,1,37,1,37,1,37,1,37,3,37,333,8,37,1,38,1,38,1,38,1,
        38,1,38,1,38,1,38,3,38,342,8,38,1,39,1,39,1,40,1,40,1,40,1,40,1,
        40,1,40,1,40,1,40,1,40,3,40,355,8,40,1,40,0,0,41,0,2,4,6,8,10,12,
        14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44,46,48,50,52,54,56,
        58,60,62,64,66,68,70,72,74,76,78,80,0,10,1,0,21,22,1,0,7,14,3,0,
        2,2,24,29,31,41,2,0,18,18,60,60,2,0,3,3,50,50,2,0,15,22,60,60,1,
        0,31,32,1,0,55,56,1,0,57,58,3,0,15,20,24,29,36,37,382,0,82,1,0,0,
        0,2,85,1,0,0,0,4,100,1,0,0,0,6,102,1,0,0,0,8,106,1,0,0,0,10,121,
        1,0,0,0,12,126,1,0,0,0,14,128,1,0,0,0,16,134,1,0,0,0,18,139,1,0,
        0,0,20,143,1,0,0,0,22,147,1,0,0,0,24,149,1,0,0,0,26,152,1,0,0,0,
        28,172,1,0,0,0,30,182,1,0,0,0,32,184,1,0,0,0,34,186,1,0,0,0,36,190,
        1,0,0,0,38,202,1,0,0,0,40,204,1,0,0,0,42,213,1,0,0,0,44,219,1,0,
        0,0,46,223,1,0,0,0,48,229,1,0,0,0,50,248,1,0,0,0,52,250,1,0,0,0,
        54,254,1,0,0,0,56,272,1,0,0,0,58,274,1,0,0,0,60,295,1,0,0,0,62,301,
        1,0,0,0,64,303,1,0,0,0,66,305,1,0,0,0,68,307,1,0,0,0,70,310,1,0,
        0,0,72,313,1,0,0,0,74,332,1,0,0,0,76,341,1,0,0,0,78,343,1,0,0,0,
        80,354,1,0,0,0,82,83,3,2,1,0,83,84,5,0,0,1,84,1,1,0,0,0,85,86,3,
        12,6,0,86,3,1,0,0,0,87,88,5,43,0,0,88,93,3,6,3,0,89,90,5,47,0,0,
        90,92,3,6,3,0,91,89,1,0,0,0,92,95,1,0,0,0,93,91,1,0,0,0,93,94,1,
        0,0,0,94,96,1,0,0,0,95,93,1,0,0,0,96,97,5,44,0,0,97,101,1,0,0,0,
        98,99,5,43,0,0,99,101,5,44,0,0,100,87,1,0,0,0,100,98,1,0,0,0,101,
        5,1,0,0,0,102,103,3,8,4,0,103,104,5,4,0,0,104,105,3,12,6,0,105,7,
        1,0,0,0,106,107,5,52,0,0,107,9,1,0,0,0,108,109,5,45,0,0,109,114,
        3,12,6,0,110,111,5,47,0,0,111,113,3,12,6,0,112,110,1,0,0,0,113,116,
        1,0,0,0,114,112,1,0,0,0,114,115,1,0,0,0,115,117,1,0,0,0,116,114,
        1,0,0,0,117,118,5,46,0,0,118,122,1,0,0,0,119,120,5,45,0,0,120,122,
        5,46,0,0,121,108,1,0,0,0,121,119,1,0,0,0,122,11,1,0,0,0,123,127,
        3,4,2,0,124,127,3,10,5,0,125,127,3,26,13,0,126,123,1,0,0,0,126,124,
        1,0,0,0,126,125,1,0,0,0,127,13,1,0,0,0,128,130,3,8,4,0,129,131,3,
        24,12,0,130,129,1,0,0,0,130,131,1,0,0,0,131,15,1,0,0,0,132,135,3,
        64,32,0,133,135,3,66,33,0,134,132,1,0,0,0,134,133,1,0,0,0,135,137,
        1,0,0,0,136,138,3,24,12,0,137,136,1,0,0,0,137,138,1,0,0,0,138,17,
        1,0,0,0,139,141,5,57,0,0,140,142,3,24,12,0,141,140,1,0,0,0,141,142,
        1,0,0,0,142,19,1,0,0,0,143,145,7,0,0,0,144,146,3,24,12,0,145,144,
        1,0,0,0,145,146,1,0,0,0,146,21,1,0,0,0,147,148,5,42,0,0,148,23,1,
        0,0,0,149,150,7,1,0,0,150,25,1,0,0,0,151,153,5,30,0,0,152,151,1,
        0,0,0,152,153,1,0,0,0,153,154,1,0,0,0,154,160,3,28,14,0,155,156,
        3,32,16,0,156,157,3,28,14,0,157,159,1,0,0,0,158,155,1,0,0,0,159,
        162,1,0,0,0,160,158,1,0,0,0,160,161,1,0,0,0,161,27,1,0,0,0,162,160,
        1,0,0,0,163,173,3,30,15,0,164,165,5,30,0,0,165,173,3,28,14,0,166,
        167,5,48,0,0,167,168,3,26,13,0,168,170,5,49,0,0,169,171,3,24,12,
        0,170,169,1,0,0,0,170,171,1,0,0,0,171,173,1,0,0,0,172,163,1,0,0,
        0,172,164,1,0,0,0,172,166,1,0,0,0,173,29,1,0,0,0,174,183,3,36,18,
        0,175,183,3,20,10,0,176,183,3,14,7,0,177,183,3,18,9,0,178,183,3,
        16,8,0,179,183,3,22,11,0,180,183,3,42,21,0,181,183,3,34,17,0,182,
        174,1,0,0,0,182,175,1,0,0,0,182,176,1,0,0,0,182,177,1,0,0,0,182,
        178,1,0,0,0,182,179,1,0,0,0,182,180,1,0,0,0,182,181,1,0,0,0,183,
        31,1,0,0,0,184,185,7,2,0,0,185,33,1,0,0,0,186,188,5,62,0,0,187,189,
        3,24,12,0,188,187,1,0,0,0,188,189,1,0,0,0,189,35,1,0,0,0,190,191,
        3,38,19,0,191,193,5,48,0,0,192,194,3,40,20,0,193,192,1,0,0,0,193,
        194,1,0,0,0,194,195,1,0,0,0,195,197,5,49,0,0,196,198,3,24,12,0,197,
        196,1,0,0,0,197,198,1,0,0,0,198,200,1,0,0,0,199,201,3,4,2,0,200,
        199,1,0,0,0,200,201,1,0,0,0,201,37,1,0,0,0,202,203,7,3,0,0,203,39,
        1,0,0,0,204,209,3,12,6,0,205,206,5,47,0,0,206,208,3,12,6,0,207,205,
        1,0,0,0,208,211,1,0,0,0,209,207,1,0,0,0,209,210,1,0,0,0,210,41,1,
        0,0,0,211,209,1,0,0,0,212,214,5,62,0,0,213,212,1,0,0,0,213,214,1,
        0,0,0,214,215,1,0,0,0,215,217,3,44,22,0,216,218,3,24,12,0,217,216,
        1,0,0,0,217,218,1,0,0,0,218,43,1,0,0,0,219,221,5,50,0,0,220,222,
        3,50,25,0,221,220,1,0,0,0,221,222,1,0,0,0,222,45,1,0,0,0,223,225,
        7,4,0,0,224,226,3,50,25,0,225,224,1,0,0,0,225,226,1,0,0,0,226,47,
        1,0,0,0,227,230,3,46,23,0,228,230,3,80,40,0,229,227,1,0,0,0,229,
        228,1,0,0,0,230,49,1,0,0,0,231,234,5,6,0,0,232,235,3,56,28,0,233,
        235,3,52,26,0,234,232,1,0,0,0,234,233,1,0,0,0,235,237,1,0,0,0,236,
        238,3,50,25,0,237,236,1,0,0,0,237,238,1,0,0,0,238,249,1,0,0,0,239,
        240,5,1,0,0,240,242,3,56,28,0,241,243,3,50,25,0,242,241,1,0,0,0,
        242,243,1,0,0,0,243,249,1,0,0,0,244,246,3,52,26,0,245,247,3,50,25,
        0,246,245,1,0,0,0,246,247,1,0,0,0,247,249,1,0,0,0,248,231,1,0,0,
        0,248,239,1,0,0,0,248,244,1,0,0,0,249,51,1,0,0,0,250,251,5,45,0,
        0,251,252,3,60,30,0,252,253,5,46,0,0,253,53,1,0,0,0,254,263,5,48,
        0,0,255,260,3,48,24,0,256,257,5,47,0,0,257,259,3,48,24,0,258,256,
        1,0,0,0,259,262,1,0,0,0,260,258,1,0,0,0,260,261,1,0,0,0,261,264,
        1,0,0,0,262,260,1,0,0,0,263,255,1,0,0,0,263,264,1,0,0,0,264,265,
        1,0,0,0,265,266,5,49,0,0,266,55,1,0,0,0,267,269,3,58,29,0,268,270,
        3,54,27,0,269,268,1,0,0,0,269,270,1,0,0,0,270,273,1,0,0,0,271,273,
        5,2,0,0,272,267,1,0,0,0,272,271,1,0,0,0,273,57,1,0,0,0,274,275,7,
        5,0,0,275,59,1,0,0,0,276,296,5,52,0,0,277,296,3,62,31,0,278,296,
        5,2,0,0,279,280,5,51,0,0,280,281,5,48,0,0,281,282,3,74,37,0,282,
        283,5,49,0,0,283,296,1,0,0,0,284,289,3,46,23,0,285,287,7,6,0,0,286,
        285,1,0,0,0,286,287,1,0,0,0,287,288,1,0,0,0,288,290,5,55,0,0,289,
        286,1,0,0,0,289,290,1,0,0,0,290,296,1,0,0,0,291,293,5,61,0,0,292,
        294,3,54,27,0,293,292,1,0,0,0,293,294,1,0,0,0,294,296,1,0,0,0,295,
        276,1,0,0,0,295,277,1,0,0,0,295,278,1,0,0,0,295,279,1,0,0,0,295,
        284,1,0,0,0,295,291,1,0,0,0,296,61,1,0,0,0,297,302,3,64,32,0,298,
        302,3,68,34,0,299,302,3,70,35,0,300,302,3,72,36,0,301,297,1,0,0,
        0,301,298,1,0,0,0,301,299,1,0,0,0,301,300,1,0,0,0,302,63,1,0,0,0,
        303,304,7,7,0,0,304,65,1,0,0,0,305,306,7,8,0,0,306,67,1,0,0,0,307,
        308,3,64,32,0,308,309,5,4,0,0,309,69,1,0,0,0,310,311,5,4,0,0,311,
        312,3,64,32,0,312,71,1,0,0,0,313,314,3,64,32,0,314,315,5,4,0,0,315,
        316,3,64,32,0,316,73,1,0,0,0,317,319,5,30,0,0,318,317,1,0,0,0,318,
        319,1,0,0,0,319,320,1,0,0,0,320,324,3,76,38,0,321,322,3,78,39,0,
        322,323,3,76,38,0,323,325,1,0,0,0,324,321,1,0,0,0,325,326,1,0,0,
        0,326,324,1,0,0,0,326,327,1,0,0,0,327,333,1,0,0,0,328,329,5,48,0,
        0,329,330,3,76,38,0,330,331,5,49,0,0,331,333,1,0,0,0,332,318,1,0,
        0,0,332,328,1,0,0,0,333,75,1,0,0,0,334,342,3,48,24,0,335,336,5,30,
        0,0,336,342,3,76,38,0,337,338,5,48,0,0,338,339,3,76,38,0,339,340,
        5,49,0,0,340,342,1,0,0,0,341,334,1,0,0,0,341,335,1,0,0,0,341,337,
        1,0,0,0,342,77,1,0,0,0,343,344,7,9,0,0,344,79,1,0,0,0,345,355,5,
        52,0,0,346,355,5,61,0,0,347,355,3,64,32,0,348,355,5,21,0,0,349,355,
        5,22,0,0,350,355,5,42,0,0,351,355,3,4,2,0,352,355,3,10,5,0,353,355,
        3,34,17,0,354,345,1,0,0,0,354,346,1,0,0,0,354,347,1,0,0,0,354,348,
        1,0,0,0,354,349,1,0,0,0,354,350,1,0,0,0,354,351,1,0,0,0,354,352,
        1,0,0,0,354,353,1,0,0,0,355,81,1,0,0,0,44,93,100,114,121,126,130,
        134,137,141,145,152,160,170,172,182,188,193,197,200,209,213,217,
        221,225,229,234,237,242,246,248,260,263,269,272,286,289,293,295,
        301,318,326,332,341,354
    ]

class JsltParser ( Parser ):

    grammarFileName = "JsltParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'.'", "'*'", "'@'", "':'", "'#'", "'..'", 
                     "'#uri'", "'#time'", "'#datetime'", "'#string'", "'#boolean'", 
                     "'#uuid'", "'#integer'", "'#decimal'", "'in'", "'nin'", 
                     "'subsetof'", "'contains'", "'size'", "'empty'", "'true'", 
                     "'false'", "'default'", "'=='", "'!='", "'>'", "'<'", 
                     "'<='", "'>='", "'!'", "'+'", "'-'", "'/'", "'%'", 
                     "'^'", "'&'", "'|'", "'&&'", "'||'", "'??'", "'->'", 
                     "'null'", "'{'", "'}'", "'['", "']'", "','", "'('", 
                     "')'", "'$'", "'?'", "<INVALID>", "<INVALID>", "'''" ]

    symbolicNames = [ "<INVALID>", "SUBSCRIPT", "WILDCARD_SUBSCRIPT", "CURRENT_VALUE", 
                      "COLON", "SHARP", "RECURSIVE_DESCENT", "URI_TYPE", 
                      "TIME_TYPE", "DATETIME_TYPE", "STRING_TYPE", "BOOLEAN_TYPE", 
                      "GUID_TYPE", "INTEGER_TYPE", "DECIMAL_TYPE", "IN", 
                      "NIN", "SUBSETOF", "CONTAINS", "SIZE", "EMPTY", "TRUE", 
                      "FALSE", "DEFAULT", "EQ", "NE", "GT", "LT", "LE", 
                      "GE", "NT", "PLUS", "MINUS", "DIVID", "MODULO", "POWER", 
                      "AND", "OR", "AND_EXCLUSIVE", "OR_EXCLUSIVE", "COALESCE", 
                      "CHAIN", "NULL", "BRACE_LEFT", "BRACE_RIGHT", "BRACKET_LEFT", 
                      "BRACKET_RIGHT", "COMMA", "PAREN_LEFT", "PAREN_RIGHT", 
                      "DOLLAR", "QUESTION", "STRING", "MULTI_LINE_COMMENT", 
                      "SINGLE_QUOTE_CODE_STRING", "NUMBER", "SIGNED_NUMBER", 
                      "INT", "SIGNED_INT", "WS", "ID", "IDQUOTED", "VARIABLE_NAME", 
                      "IDLOWCASE" ]

    RULE_script = 0
    RULE_json = 1
    RULE_obj = 2
    RULE_pair = 3
    RULE_string = 4
    RULE_array = 5
    RULE_jsonValue = 6
    RULE_jsonValueString = 7
    RULE_jsonValueNumber = 8
    RULE_jsonValueInteger = 9
    RULE_jsonValueBoolean = 10
    RULE_jsonValueNull = 11
    RULE_jsonType = 12
    RULE_jsonLtOperations = 13
    RULE_jsonLtOperation = 14
    RULE_jsonLtItem = 15
    RULE_operation = 16
    RULE_variable = 17
    RULE_jsonfunctionCall = 18
    RULE_jsonfunctionName = 19
    RULE_jsonValueList = 20
    RULE_jsltJsonpath = 21
    RULE_jsonpath = 22
    RULE_jsonpath_ = 23
    RULE_jsonpath__ = 24
    RULE_jsonpath_subscript = 25
    RULE_subscriptables = 26
    RULE_subscriptableArguments = 27
    RULE_subscriptableBareword = 28
    RULE_jsonPath_identifier = 29
    RULE_subscriptable = 30
    RULE_sliceable = 31
    RULE_signedNumber = 32
    RULE_signedInt = 33
    RULE_sliceableLeft = 34
    RULE_sliceableRight = 35
    RULE_sliceableBinary = 36
    RULE_expressions = 37
    RULE_expression = 38
    RULE_binaryOperator = 39
    RULE_value = 40

    ruleNames =  [ "script", "json", "obj", "pair", "string", "array", "jsonValue", 
                   "jsonValueString", "jsonValueNumber", "jsonValueInteger", 
                   "jsonValueBoolean", "jsonValueNull", "jsonType", "jsonLtOperations", 
                   "jsonLtOperation", "jsonLtItem", "operation", "variable", 
                   "jsonfunctionCall", "jsonfunctionName", "jsonValueList", 
                   "jsltJsonpath", "jsonpath", "jsonpath_", "jsonpath__", 
                   "jsonpath_subscript", "subscriptables", "subscriptableArguments", 
                   "subscriptableBareword", "jsonPath_identifier", "subscriptable", 
                   "sliceable", "signedNumber", "signedInt", "sliceableLeft", 
                   "sliceableRight", "sliceableBinary", "expressions", "expression", 
                   "binaryOperator", "value" ]

    EOF = Token.EOF
    SUBSCRIPT=1
    WILDCARD_SUBSCRIPT=2
    CURRENT_VALUE=3
    COLON=4
    SHARP=5
    RECURSIVE_DESCENT=6
    URI_TYPE=7
    TIME_TYPE=8
    DATETIME_TYPE=9
    STRING_TYPE=10
    BOOLEAN_TYPE=11
    GUID_TYPE=12
    INTEGER_TYPE=13
    DECIMAL_TYPE=14
    IN=15
    NIN=16
    SUBSETOF=17
    CONTAINS=18
    SIZE=19
    EMPTY=20
    TRUE=21
    FALSE=22
    DEFAULT=23
    EQ=24
    NE=25
    GT=26
    LT=27
    LE=28
    GE=29
    NT=30
    PLUS=31
    MINUS=32
    DIVID=33
    MODULO=34
    POWER=35
    AND=36
    OR=37
    AND_EXCLUSIVE=38
    OR_EXCLUSIVE=39
    COALESCE=40
    CHAIN=41
    NULL=42
    BRACE_LEFT=43
    BRACE_RIGHT=44
    BRACKET_LEFT=45
    BRACKET_RIGHT=46
    COMMA=47
    PAREN_LEFT=48
    PAREN_RIGHT=49
    DOLLAR=50
    QUESTION=51
    STRING=52
    MULTI_LINE_COMMENT=53
    SINGLE_QUOTE_CODE_STRING=54
    NUMBER=55
    SIGNED_NUMBER=56
    INT=57
    SIGNED_INT=58
    WS=59
    ID=60
    IDQUOTED=61
    VARIABLE_NAME=62
    IDLOWCASE=63

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ScriptContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def json(self):
            return self.getTypedRuleContext(JsltParser.JsonContext,0)


        def EOF(self):
            return self.getToken(JsltParser.EOF, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_script

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterScript" ):
                listener.enterScript(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitScript" ):
                listener.exitScript(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitScript" ):
                return visitor.visitScript(self)
            else:
                return visitor.visitChildren(self)




    def script(self):

        localctx = JsltParser.ScriptContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_script)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.json()
            self.state = 83
            self.match(JsltParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def jsonValue(self):
            return self.getTypedRuleContext(JsltParser.JsonValueContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_json

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJson" ):
                listener.enterJson(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJson" ):
                listener.exitJson(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJson" ):
                return visitor.visitJson(self)
            else:
                return visitor.visitChildren(self)




    def json(self):

        localctx = JsltParser.JsonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_json)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 85
            self.jsonValue()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ObjContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BRACE_LEFT(self):
            return self.getToken(JsltParser.BRACE_LEFT, 0)

        def pair(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JsltParser.PairContext)
            else:
                return self.getTypedRuleContext(JsltParser.PairContext,i)


        def BRACE_RIGHT(self):
            return self.getToken(JsltParser.BRACE_RIGHT, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(JsltParser.COMMA)
            else:
                return self.getToken(JsltParser.COMMA, i)

        def getRuleIndex(self):
            return JsltParser.RULE_obj

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterObj" ):
                listener.enterObj(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitObj" ):
                listener.exitObj(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitObj" ):
                return visitor.visitObj(self)
            else:
                return visitor.visitChildren(self)




    def obj(self):

        localctx = JsltParser.ObjContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_obj)
        self._la = 0 # Token type
        try:
            self.state = 100
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 87
                self.match(JsltParser.BRACE_LEFT)
                self.state = 88
                self.pair()
                self.state = 93
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==47:
                    self.state = 89
                    self.match(JsltParser.COMMA)
                    self.state = 90
                    self.pair()
                    self.state = 95
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 96
                self.match(JsltParser.BRACE_RIGHT)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 98
                self.match(JsltParser.BRACE_LEFT)
                self.state = 99
                self.match(JsltParser.BRACE_RIGHT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PairContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def string(self):
            return self.getTypedRuleContext(JsltParser.StringContext,0)


        def COLON(self):
            return self.getToken(JsltParser.COLON, 0)

        def jsonValue(self):
            return self.getTypedRuleContext(JsltParser.JsonValueContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_pair

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPair" ):
                listener.enterPair(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPair" ):
                listener.exitPair(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitPair" ):
                return visitor.visitPair(self)
            else:
                return visitor.visitChildren(self)




    def pair(self):

        localctx = JsltParser.PairContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_pair)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 102
            self.string()
            self.state = 103
            self.match(JsltParser.COLON)
            self.state = 104
            self.jsonValue()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(JsltParser.STRING, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_string

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterString" ):
                listener.enterString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitString" ):
                listener.exitString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitString" ):
                return visitor.visitString(self)
            else:
                return visitor.visitChildren(self)




    def string(self):

        localctx = JsltParser.StringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_string)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 106
            self.match(JsltParser.STRING)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArrayContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BRACKET_LEFT(self):
            return self.getToken(JsltParser.BRACKET_LEFT, 0)

        def jsonValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JsltParser.JsonValueContext)
            else:
                return self.getTypedRuleContext(JsltParser.JsonValueContext,i)


        def BRACKET_RIGHT(self):
            return self.getToken(JsltParser.BRACKET_RIGHT, 0)

        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(JsltParser.COMMA)
            else:
                return self.getToken(JsltParser.COMMA, i)

        def getRuleIndex(self):
            return JsltParser.RULE_array

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArray" ):
                listener.enterArray(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArray" ):
                listener.exitArray(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArray" ):
                return visitor.visitArray(self)
            else:
                return visitor.visitChildren(self)




    def array(self):

        localctx = JsltParser.ArrayContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_array)
        self._la = 0 # Token type
        try:
            self.state = 121
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 108
                self.match(JsltParser.BRACKET_LEFT)
                self.state = 109
                self.jsonValue()
                self.state = 114
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==47:
                    self.state = 110
                    self.match(JsltParser.COMMA)
                    self.state = 111
                    self.jsonValue()
                    self.state = 116
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)

                self.state = 117
                self.match(JsltParser.BRACKET_RIGHT)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 119
                self.match(JsltParser.BRACKET_LEFT)
                self.state = 120
                self.match(JsltParser.BRACKET_RIGHT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def obj(self):
            return self.getTypedRuleContext(JsltParser.ObjContext,0)


        def array(self):
            return self.getTypedRuleContext(JsltParser.ArrayContext,0)


        def jsonLtOperations(self):
            return self.getTypedRuleContext(JsltParser.JsonLtOperationsContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonValue

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonValue" ):
                listener.enterJsonValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonValue" ):
                listener.exitJsonValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonValue" ):
                return visitor.visitJsonValue(self)
            else:
                return visitor.visitChildren(self)




    def jsonValue(self):

        localctx = JsltParser.JsonValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_jsonValue)
        try:
            self.state = 126
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [43]:
                self.enterOuterAlt(localctx, 1)
                self.state = 123
                self.obj()
                pass
            elif token in [45]:
                self.enterOuterAlt(localctx, 2)
                self.state = 124
                self.array()
                pass
            elif token in [18, 21, 22, 30, 42, 48, 50, 52, 55, 56, 57, 58, 60, 62]:
                self.enterOuterAlt(localctx, 3)
                self.state = 125
                self.jsonLtOperations()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonValueStringContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def string(self):
            return self.getTypedRuleContext(JsltParser.StringContext,0)


        def jsonType(self):
            return self.getTypedRuleContext(JsltParser.JsonTypeContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonValueString

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonValueString" ):
                listener.enterJsonValueString(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonValueString" ):
                listener.exitJsonValueString(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonValueString" ):
                return visitor.visitJsonValueString(self)
            else:
                return visitor.visitChildren(self)




    def jsonValueString(self):

        localctx = JsltParser.JsonValueStringContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_jsonValueString)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            self.string()
            self.state = 130
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0):
                self.state = 129
                self.jsonType()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonValueNumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def signedNumber(self):
            return self.getTypedRuleContext(JsltParser.SignedNumberContext,0)


        def signedInt(self):
            return self.getTypedRuleContext(JsltParser.SignedIntContext,0)


        def jsonType(self):
            return self.getTypedRuleContext(JsltParser.JsonTypeContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonValueNumber

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonValueNumber" ):
                listener.enterJsonValueNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonValueNumber" ):
                listener.exitJsonValueNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonValueNumber" ):
                return visitor.visitJsonValueNumber(self)
            else:
                return visitor.visitChildren(self)




    def jsonValueNumber(self):

        localctx = JsltParser.JsonValueNumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_jsonValueNumber)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 134
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [55, 56]:
                self.state = 132
                self.signedNumber()
                pass
            elif token in [57, 58]:
                self.state = 133
                self.signedInt()
                pass
            else:
                raise NoViableAltException(self)

            self.state = 137
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0):
                self.state = 136
                self.jsonType()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonValueIntegerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def INT(self):
            return self.getToken(JsltParser.INT, 0)

        def jsonType(self):
            return self.getTypedRuleContext(JsltParser.JsonTypeContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonValueInteger

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonValueInteger" ):
                listener.enterJsonValueInteger(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonValueInteger" ):
                listener.exitJsonValueInteger(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonValueInteger" ):
                return visitor.visitJsonValueInteger(self)
            else:
                return visitor.visitChildren(self)




    def jsonValueInteger(self):

        localctx = JsltParser.JsonValueIntegerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_jsonValueInteger)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 139
            self.match(JsltParser.INT)
            self.state = 141
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0):
                self.state = 140
                self.jsonType()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonValueBooleanContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRUE(self):
            return self.getToken(JsltParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(JsltParser.FALSE, 0)

        def jsonType(self):
            return self.getTypedRuleContext(JsltParser.JsonTypeContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonValueBoolean

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonValueBoolean" ):
                listener.enterJsonValueBoolean(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonValueBoolean" ):
                listener.exitJsonValueBoolean(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonValueBoolean" ):
                return visitor.visitJsonValueBoolean(self)
            else:
                return visitor.visitChildren(self)




    def jsonValueBoolean(self):

        localctx = JsltParser.JsonValueBooleanContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_jsonValueBoolean)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 143
            _la = self._input.LA(1)
            if not(_la==21 or _la==22):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 145
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0):
                self.state = 144
                self.jsonType()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonValueNullContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NULL(self):
            return self.getToken(JsltParser.NULL, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_jsonValueNull

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonValueNull" ):
                listener.enterJsonValueNull(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonValueNull" ):
                listener.exitJsonValueNull(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonValueNull" ):
                return visitor.visitJsonValueNull(self)
            else:
                return visitor.visitChildren(self)




    def jsonValueNull(self):

        localctx = JsltParser.JsonValueNullContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_jsonValueNull)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 147
            self.match(JsltParser.NULL)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonTypeContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BOOLEAN_TYPE(self):
            return self.getToken(JsltParser.BOOLEAN_TYPE, 0)

        def URI_TYPE(self):
            return self.getToken(JsltParser.URI_TYPE, 0)

        def TIME_TYPE(self):
            return self.getToken(JsltParser.TIME_TYPE, 0)

        def DATETIME_TYPE(self):
            return self.getToken(JsltParser.DATETIME_TYPE, 0)

        def STRING_TYPE(self):
            return self.getToken(JsltParser.STRING_TYPE, 0)

        def GUID_TYPE(self):
            return self.getToken(JsltParser.GUID_TYPE, 0)

        def INTEGER_TYPE(self):
            return self.getToken(JsltParser.INTEGER_TYPE, 0)

        def DECIMAL_TYPE(self):
            return self.getToken(JsltParser.DECIMAL_TYPE, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_jsonType

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonType" ):
                listener.enterJsonType(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonType" ):
                listener.exitJsonType(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonType" ):
                return visitor.visitJsonType(self)
            else:
                return visitor.visitChildren(self)




    def jsonType(self):

        localctx = JsltParser.JsonTypeContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_jsonType)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 149
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonLtOperationsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def jsonLtOperation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JsltParser.JsonLtOperationContext)
            else:
                return self.getTypedRuleContext(JsltParser.JsonLtOperationContext,i)


        def NT(self):
            return self.getToken(JsltParser.NT, 0)

        def operation(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JsltParser.OperationContext)
            else:
                return self.getTypedRuleContext(JsltParser.OperationContext,i)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonLtOperations

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonLtOperations" ):
                listener.enterJsonLtOperations(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonLtOperations" ):
                listener.exitJsonLtOperations(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonLtOperations" ):
                return visitor.visitJsonLtOperations(self)
            else:
                return visitor.visitChildren(self)




    def jsonLtOperations(self):

        localctx = JsltParser.JsonLtOperationsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_jsonLtOperations)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,10,self._ctx)
            if la_ == 1:
                self.state = 151
                self.match(JsltParser.NT)


            self.state = 154
            self.jsonLtOperation()
            self.state = 160
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 4396955992068) != 0):
                self.state = 155
                self.operation()
                self.state = 156
                self.jsonLtOperation()
                self.state = 162
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonLtOperationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def jsonLtItem(self):
            return self.getTypedRuleContext(JsltParser.JsonLtItemContext,0)


        def NT(self):
            return self.getToken(JsltParser.NT, 0)

        def jsonLtOperation(self):
            return self.getTypedRuleContext(JsltParser.JsonLtOperationContext,0)


        def PAREN_LEFT(self):
            return self.getToken(JsltParser.PAREN_LEFT, 0)

        def jsonLtOperations(self):
            return self.getTypedRuleContext(JsltParser.JsonLtOperationsContext,0)


        def PAREN_RIGHT(self):
            return self.getToken(JsltParser.PAREN_RIGHT, 0)

        def jsonType(self):
            return self.getTypedRuleContext(JsltParser.JsonTypeContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonLtOperation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonLtOperation" ):
                listener.enterJsonLtOperation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonLtOperation" ):
                listener.exitJsonLtOperation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonLtOperation" ):
                return visitor.visitJsonLtOperation(self)
            else:
                return visitor.visitChildren(self)




    def jsonLtOperation(self):

        localctx = JsltParser.JsonLtOperationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_jsonLtOperation)
        self._la = 0 # Token type
        try:
            self.state = 172
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [18, 21, 22, 42, 50, 52, 55, 56, 57, 58, 60, 62]:
                self.enterOuterAlt(localctx, 1)
                self.state = 163
                self.jsonLtItem()
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 2)
                self.state = 164
                self.match(JsltParser.NT)
                self.state = 165
                self.jsonLtOperation()
                pass
            elif token in [48]:
                self.enterOuterAlt(localctx, 3)
                self.state = 166
                self.match(JsltParser.PAREN_LEFT)
                self.state = 167
                self.jsonLtOperations()
                self.state = 168
                self.match(JsltParser.PAREN_RIGHT)
                self.state = 170
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0):
                    self.state = 169
                    self.jsonType()


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonLtItemContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def jsonfunctionCall(self):
            return self.getTypedRuleContext(JsltParser.JsonfunctionCallContext,0)


        def jsonValueBoolean(self):
            return self.getTypedRuleContext(JsltParser.JsonValueBooleanContext,0)


        def jsonValueString(self):
            return self.getTypedRuleContext(JsltParser.JsonValueStringContext,0)


        def jsonValueInteger(self):
            return self.getTypedRuleContext(JsltParser.JsonValueIntegerContext,0)


        def jsonValueNumber(self):
            return self.getTypedRuleContext(JsltParser.JsonValueNumberContext,0)


        def jsonValueNull(self):
            return self.getTypedRuleContext(JsltParser.JsonValueNullContext,0)


        def jsltJsonpath(self):
            return self.getTypedRuleContext(JsltParser.JsltJsonpathContext,0)


        def variable(self):
            return self.getTypedRuleContext(JsltParser.VariableContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonLtItem

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonLtItem" ):
                listener.enterJsonLtItem(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonLtItem" ):
                listener.exitJsonLtItem(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonLtItem" ):
                return visitor.visitJsonLtItem(self)
            else:
                return visitor.visitChildren(self)




    def jsonLtItem(self):

        localctx = JsltParser.JsonLtItemContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_jsonLtItem)
        try:
            self.state = 182
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,14,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 174
                self.jsonfunctionCall()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 175
                self.jsonValueBoolean()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 176
                self.jsonValueString()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 177
                self.jsonValueInteger()
                pass

            elif la_ == 5:
                self.enterOuterAlt(localctx, 5)
                self.state = 178
                self.jsonValueNumber()
                pass

            elif la_ == 6:
                self.enterOuterAlt(localctx, 6)
                self.state = 179
                self.jsonValueNull()
                pass

            elif la_ == 7:
                self.enterOuterAlt(localctx, 7)
                self.state = 180
                self.jsltJsonpath()
                pass

            elif la_ == 8:
                self.enterOuterAlt(localctx, 8)
                self.state = 181
                self.variable()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperationContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(JsltParser.EQ, 0)

        def GE(self):
            return self.getToken(JsltParser.GE, 0)

        def GT(self):
            return self.getToken(JsltParser.GT, 0)

        def LE(self):
            return self.getToken(JsltParser.LE, 0)

        def LT(self):
            return self.getToken(JsltParser.LT, 0)

        def NE(self):
            return self.getToken(JsltParser.NE, 0)

        def PLUS(self):
            return self.getToken(JsltParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(JsltParser.MINUS, 0)

        def DIVID(self):
            return self.getToken(JsltParser.DIVID, 0)

        def MODULO(self):
            return self.getToken(JsltParser.MODULO, 0)

        def WILDCARD_SUBSCRIPT(self):
            return self.getToken(JsltParser.WILDCARD_SUBSCRIPT, 0)

        def POWER(self):
            return self.getToken(JsltParser.POWER, 0)

        def CHAIN(self):
            return self.getToken(JsltParser.CHAIN, 0)

        def AND(self):
            return self.getToken(JsltParser.AND, 0)

        def OR(self):
            return self.getToken(JsltParser.OR, 0)

        def AND_EXCLUSIVE(self):
            return self.getToken(JsltParser.AND_EXCLUSIVE, 0)

        def OR_EXCLUSIVE(self):
            return self.getToken(JsltParser.OR_EXCLUSIVE, 0)

        def COALESCE(self):
            return self.getToken(JsltParser.COALESCE, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_operation

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperation" ):
                listener.enterOperation(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperation" ):
                listener.exitOperation(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOperation" ):
                return visitor.visitOperation(self)
            else:
                return visitor.visitChildren(self)




    def operation(self):

        localctx = JsltParser.OperationContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_operation)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 184
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 4396955992068) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class VariableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def VARIABLE_NAME(self):
            return self.getToken(JsltParser.VARIABLE_NAME, 0)

        def jsonType(self):
            return self.getTypedRuleContext(JsltParser.JsonTypeContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_variable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterVariable" ):
                listener.enterVariable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitVariable" ):
                listener.exitVariable(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitVariable" ):
                return visitor.visitVariable(self)
            else:
                return visitor.visitChildren(self)




    def variable(self):

        localctx = JsltParser.VariableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_variable)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 186
            self.match(JsltParser.VARIABLE_NAME)
            self.state = 188
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0):
                self.state = 187
                self.jsonType()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonfunctionCallContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def jsonfunctionName(self):
            return self.getTypedRuleContext(JsltParser.JsonfunctionNameContext,0)


        def PAREN_LEFT(self):
            return self.getToken(JsltParser.PAREN_LEFT, 0)

        def PAREN_RIGHT(self):
            return self.getToken(JsltParser.PAREN_RIGHT, 0)

        def jsonValueList(self):
            return self.getTypedRuleContext(JsltParser.JsonValueListContext,0)


        def jsonType(self):
            return self.getTypedRuleContext(JsltParser.JsonTypeContext,0)


        def obj(self):
            return self.getTypedRuleContext(JsltParser.ObjContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonfunctionCall

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonfunctionCall" ):
                listener.enterJsonfunctionCall(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonfunctionCall" ):
                listener.exitJsonfunctionCall(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonfunctionCall" ):
                return visitor.visitJsonfunctionCall(self)
            else:
                return visitor.visitChildren(self)




    def jsonfunctionCall(self):

        localctx = JsltParser.JsonfunctionCallContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_jsonfunctionCall)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 190
            self.jsonfunctionName()
            self.state = 191
            self.match(JsltParser.PAREN_LEFT)
            self.state = 193
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 6310998832421535744) != 0):
                self.state = 192
                self.jsonValueList()


            self.state = 195
            self.match(JsltParser.PAREN_RIGHT)
            self.state = 197
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0):
                self.state = 196
                self.jsonType()


            self.state = 200
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==43:
                self.state = 199
                self.obj()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonfunctionNameContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(JsltParser.ID, 0)

        def CONTAINS(self):
            return self.getToken(JsltParser.CONTAINS, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_jsonfunctionName

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonfunctionName" ):
                listener.enterJsonfunctionName(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonfunctionName" ):
                listener.exitJsonfunctionName(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonfunctionName" ):
                return visitor.visitJsonfunctionName(self)
            else:
                return visitor.visitChildren(self)




    def jsonfunctionName(self):

        localctx = JsltParser.JsonfunctionNameContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_jsonfunctionName)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 202
            _la = self._input.LA(1)
            if not(_la==18 or _la==60):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonValueListContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def jsonValue(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JsltParser.JsonValueContext)
            else:
                return self.getTypedRuleContext(JsltParser.JsonValueContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(JsltParser.COMMA)
            else:
                return self.getToken(JsltParser.COMMA, i)

        def getRuleIndex(self):
            return JsltParser.RULE_jsonValueList

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonValueList" ):
                listener.enterJsonValueList(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonValueList" ):
                listener.exitJsonValueList(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonValueList" ):
                return visitor.visitJsonValueList(self)
            else:
                return visitor.visitChildren(self)




    def jsonValueList(self):

        localctx = JsltParser.JsonValueListContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_jsonValueList)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 204
            self.jsonValue()
            self.state = 209
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==47:
                self.state = 205
                self.match(JsltParser.COMMA)
                self.state = 206
                self.jsonValue()
                self.state = 211
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsltJsonpathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def jsonpath(self):
            return self.getTypedRuleContext(JsltParser.JsonpathContext,0)


        def VARIABLE_NAME(self):
            return self.getToken(JsltParser.VARIABLE_NAME, 0)

        def jsonType(self):
            return self.getTypedRuleContext(JsltParser.JsonTypeContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsltJsonpath

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsltJsonpath" ):
                listener.enterJsltJsonpath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsltJsonpath" ):
                listener.exitJsltJsonpath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsltJsonpath" ):
                return visitor.visitJsltJsonpath(self)
            else:
                return visitor.visitChildren(self)




    def jsltJsonpath(self):

        localctx = JsltParser.JsltJsonpathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_jsltJsonpath)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 213
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==62:
                self.state = 212
                self.match(JsltParser.VARIABLE_NAME)


            self.state = 215
            self.jsonpath()
            self.state = 217
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 32640) != 0):
                self.state = 216
                self.jsonType()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonpathContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOLLAR(self):
            return self.getToken(JsltParser.DOLLAR, 0)

        def jsonpath_subscript(self):
            return self.getTypedRuleContext(JsltParser.Jsonpath_subscriptContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonpath

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonpath" ):
                listener.enterJsonpath(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonpath" ):
                listener.exitJsonpath(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonpath" ):
                return visitor.visitJsonpath(self)
            else:
                return visitor.visitChildren(self)




    def jsonpath(self):

        localctx = JsltParser.JsonpathContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_jsonpath)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 219
            self.match(JsltParser.DOLLAR)
            self.state = 221
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 35184372088898) != 0):
                self.state = 220
                self.jsonpath_subscript()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Jsonpath_Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DOLLAR(self):
            return self.getToken(JsltParser.DOLLAR, 0)

        def CURRENT_VALUE(self):
            return self.getToken(JsltParser.CURRENT_VALUE, 0)

        def jsonpath_subscript(self):
            return self.getTypedRuleContext(JsltParser.Jsonpath_subscriptContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonpath_

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonpath_" ):
                listener.enterJsonpath_(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonpath_" ):
                listener.exitJsonpath_(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonpath_" ):
                return visitor.visitJsonpath_(self)
            else:
                return visitor.visitChildren(self)




    def jsonpath_(self):

        localctx = JsltParser.Jsonpath_Context(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_jsonpath_)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 223
            _la = self._input.LA(1)
            if not(_la==3 or _la==50):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
            self.state = 225
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 35184372088898) != 0):
                self.state = 224
                self.jsonpath_subscript()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Jsonpath__Context(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def jsonpath_(self):
            return self.getTypedRuleContext(JsltParser.Jsonpath_Context,0)


        def value(self):
            return self.getTypedRuleContext(JsltParser.ValueContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_jsonpath__

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonpath__" ):
                listener.enterJsonpath__(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonpath__" ):
                listener.exitJsonpath__(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonpath__" ):
                return visitor.visitJsonpath__(self)
            else:
                return visitor.visitChildren(self)




    def jsonpath__(self):

        localctx = JsltParser.Jsonpath__Context(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_jsonpath__)
        try:
            self.state = 229
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3, 50]:
                self.enterOuterAlt(localctx, 1)
                self.state = 227
                self.jsonpath_()
                pass
            elif token in [21, 22, 42, 43, 45, 52, 55, 56, 61, 62]:
                self.enterOuterAlt(localctx, 2)
                self.state = 228
                self.value()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Jsonpath_subscriptContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RECURSIVE_DESCENT(self):
            return self.getToken(JsltParser.RECURSIVE_DESCENT, 0)

        def subscriptableBareword(self):
            return self.getTypedRuleContext(JsltParser.SubscriptableBarewordContext,0)


        def subscriptables(self):
            return self.getTypedRuleContext(JsltParser.SubscriptablesContext,0)


        def jsonpath_subscript(self):
            return self.getTypedRuleContext(JsltParser.Jsonpath_subscriptContext,0)


        def SUBSCRIPT(self):
            return self.getToken(JsltParser.SUBSCRIPT, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_jsonpath_subscript

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonpath_subscript" ):
                listener.enterJsonpath_subscript(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonpath_subscript" ):
                listener.exitJsonpath_subscript(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonpath_subscript" ):
                return visitor.visitJsonpath_subscript(self)
            else:
                return visitor.visitChildren(self)




    def jsonpath_subscript(self):

        localctx = JsltParser.Jsonpath_subscriptContext(self, self._ctx, self.state)
        self.enterRule(localctx, 50, self.RULE_jsonpath_subscript)
        self._la = 0 # Token type
        try:
            self.state = 248
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [6]:
                self.enterOuterAlt(localctx, 1)
                self.state = 231
                self.match(JsltParser.RECURSIVE_DESCENT)
                self.state = 234
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [2, 15, 16, 17, 18, 19, 20, 21, 22, 60]:
                    self.state = 232
                    self.subscriptableBareword()
                    pass
                elif token in [45]:
                    self.state = 233
                    self.subscriptables()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 237
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 35184372088898) != 0):
                    self.state = 236
                    self.jsonpath_subscript()


                pass
            elif token in [1]:
                self.enterOuterAlt(localctx, 2)
                self.state = 239
                self.match(JsltParser.SUBSCRIPT)
                self.state = 240
                self.subscriptableBareword()
                self.state = 242
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 35184372088898) != 0):
                    self.state = 241
                    self.jsonpath_subscript()


                pass
            elif token in [45]:
                self.enterOuterAlt(localctx, 3)
                self.state = 244
                self.subscriptables()
                self.state = 246
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 35184372088898) != 0):
                    self.state = 245
                    self.jsonpath_subscript()


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubscriptablesContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BRACKET_LEFT(self):
            return self.getToken(JsltParser.BRACKET_LEFT, 0)

        def subscriptable(self):
            return self.getTypedRuleContext(JsltParser.SubscriptableContext,0)


        def BRACKET_RIGHT(self):
            return self.getToken(JsltParser.BRACKET_RIGHT, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_subscriptables

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubscriptables" ):
                listener.enterSubscriptables(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubscriptables" ):
                listener.exitSubscriptables(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubscriptables" ):
                return visitor.visitSubscriptables(self)
            else:
                return visitor.visitChildren(self)




    def subscriptables(self):

        localctx = JsltParser.SubscriptablesContext(self, self._ctx, self.state)
        self.enterRule(localctx, 52, self.RULE_subscriptables)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 250
            self.match(JsltParser.BRACKET_LEFT)
            self.state = 251
            self.subscriptable()
            self.state = 252
            self.match(JsltParser.BRACKET_RIGHT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubscriptableArgumentsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PAREN_LEFT(self):
            return self.getToken(JsltParser.PAREN_LEFT, 0)

        def PAREN_RIGHT(self):
            return self.getToken(JsltParser.PAREN_RIGHT, 0)

        def jsonpath__(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JsltParser.Jsonpath__Context)
            else:
                return self.getTypedRuleContext(JsltParser.Jsonpath__Context,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(JsltParser.COMMA)
            else:
                return self.getToken(JsltParser.COMMA, i)

        def getRuleIndex(self):
            return JsltParser.RULE_subscriptableArguments

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubscriptableArguments" ):
                listener.enterSubscriptableArguments(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubscriptableArguments" ):
                listener.exitSubscriptableArguments(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubscriptableArguments" ):
                return visitor.visitSubscriptableArguments(self)
            else:
                return visitor.visitChildren(self)




    def subscriptableArguments(self):

        localctx = JsltParser.SubscriptableArgumentsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 54, self.RULE_subscriptableArguments)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 254
            self.match(JsltParser.PAREN_LEFT)
            self.state = 263
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if (((_la) & ~0x3f) == 0 and ((1 << _la) & 7031293296750100488) != 0):
                self.state = 255
                self.jsonpath__()
                self.state = 260
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==47:
                    self.state = 256
                    self.match(JsltParser.COMMA)
                    self.state = 257
                    self.jsonpath__()
                    self.state = 262
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 265
            self.match(JsltParser.PAREN_RIGHT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubscriptableBarewordContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def jsonPath_identifier(self):
            return self.getTypedRuleContext(JsltParser.JsonPath_identifierContext,0)


        def subscriptableArguments(self):
            return self.getTypedRuleContext(JsltParser.SubscriptableArgumentsContext,0)


        def WILDCARD_SUBSCRIPT(self):
            return self.getToken(JsltParser.WILDCARD_SUBSCRIPT, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_subscriptableBareword

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubscriptableBareword" ):
                listener.enterSubscriptableBareword(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubscriptableBareword" ):
                listener.exitSubscriptableBareword(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubscriptableBareword" ):
                return visitor.visitSubscriptableBareword(self)
            else:
                return visitor.visitChildren(self)




    def subscriptableBareword(self):

        localctx = JsltParser.SubscriptableBarewordContext(self, self._ctx, self.state)
        self.enterRule(localctx, 56, self.RULE_subscriptableBareword)
        self._la = 0 # Token type
        try:
            self.state = 272
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15, 16, 17, 18, 19, 20, 21, 22, 60]:
                self.enterOuterAlt(localctx, 1)
                self.state = 267
                self.jsonPath_identifier()
                self.state = 269
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==48:
                    self.state = 268
                    self.subscriptableArguments()


                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 271
                self.match(JsltParser.WILDCARD_SUBSCRIPT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class JsonPath_identifierContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(JsltParser.ID, 0)

        def IN(self):
            return self.getToken(JsltParser.IN, 0)

        def NIN(self):
            return self.getToken(JsltParser.NIN, 0)

        def SUBSETOF(self):
            return self.getToken(JsltParser.SUBSETOF, 0)

        def CONTAINS(self):
            return self.getToken(JsltParser.CONTAINS, 0)

        def SIZE(self):
            return self.getToken(JsltParser.SIZE, 0)

        def EMPTY(self):
            return self.getToken(JsltParser.EMPTY, 0)

        def TRUE(self):
            return self.getToken(JsltParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(JsltParser.FALSE, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_jsonPath_identifier

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterJsonPath_identifier" ):
                listener.enterJsonPath_identifier(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitJsonPath_identifier" ):
                listener.exitJsonPath_identifier(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitJsonPath_identifier" ):
                return visitor.visitJsonPath_identifier(self)
            else:
                return visitor.visitChildren(self)




    def jsonPath_identifier(self):

        localctx = JsltParser.JsonPath_identifierContext(self, self._ctx, self.state)
        self.enterRule(localctx, 58, self.RULE_jsonPath_identifier)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 274
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 1152921504615202816) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SubscriptableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(JsltParser.STRING, 0)

        def sliceable(self):
            return self.getTypedRuleContext(JsltParser.SliceableContext,0)


        def WILDCARD_SUBSCRIPT(self):
            return self.getToken(JsltParser.WILDCARD_SUBSCRIPT, 0)

        def QUESTION(self):
            return self.getToken(JsltParser.QUESTION, 0)

        def PAREN_LEFT(self):
            return self.getToken(JsltParser.PAREN_LEFT, 0)

        def expressions(self):
            return self.getTypedRuleContext(JsltParser.ExpressionsContext,0)


        def PAREN_RIGHT(self):
            return self.getToken(JsltParser.PAREN_RIGHT, 0)

        def jsonpath_(self):
            return self.getTypedRuleContext(JsltParser.Jsonpath_Context,0)


        def NUMBER(self):
            return self.getToken(JsltParser.NUMBER, 0)

        def PLUS(self):
            return self.getToken(JsltParser.PLUS, 0)

        def MINUS(self):
            return self.getToken(JsltParser.MINUS, 0)

        def IDQUOTED(self):
            return self.getToken(JsltParser.IDQUOTED, 0)

        def subscriptableArguments(self):
            return self.getTypedRuleContext(JsltParser.SubscriptableArgumentsContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_subscriptable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSubscriptable" ):
                listener.enterSubscriptable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSubscriptable" ):
                listener.exitSubscriptable(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSubscriptable" ):
                return visitor.visitSubscriptable(self)
            else:
                return visitor.visitChildren(self)




    def subscriptable(self):

        localctx = JsltParser.SubscriptableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 60, self.RULE_subscriptable)
        self._la = 0 # Token type
        try:
            self.state = 295
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [52]:
                self.enterOuterAlt(localctx, 1)
                self.state = 276
                self.match(JsltParser.STRING)
                pass
            elif token in [4, 55, 56]:
                self.enterOuterAlt(localctx, 2)
                self.state = 277
                self.sliceable()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 3)
                self.state = 278
                self.match(JsltParser.WILDCARD_SUBSCRIPT)
                pass
            elif token in [51]:
                self.enterOuterAlt(localctx, 4)
                self.state = 279
                self.match(JsltParser.QUESTION)
                self.state = 280
                self.match(JsltParser.PAREN_LEFT)
                self.state = 281
                self.expressions()
                self.state = 282
                self.match(JsltParser.PAREN_RIGHT)
                pass
            elif token in [3, 50]:
                self.enterOuterAlt(localctx, 5)
                self.state = 284
                self.jsonpath_()
                self.state = 289
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 36028803461414912) != 0):
                    self.state = 286
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==31 or _la==32:
                        self.state = 285
                        _la = self._input.LA(1)
                        if not(_la==31 or _la==32):
                            self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()


                    self.state = 288
                    self.match(JsltParser.NUMBER)


                pass
            elif token in [61]:
                self.enterOuterAlt(localctx, 6)
                self.state = 291
                self.match(JsltParser.IDQUOTED)
                self.state = 293
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==48:
                    self.state = 292
                    self.subscriptableArguments()


                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SliceableContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def signedNumber(self):
            return self.getTypedRuleContext(JsltParser.SignedNumberContext,0)


        def sliceableLeft(self):
            return self.getTypedRuleContext(JsltParser.SliceableLeftContext,0)


        def sliceableRight(self):
            return self.getTypedRuleContext(JsltParser.SliceableRightContext,0)


        def sliceableBinary(self):
            return self.getTypedRuleContext(JsltParser.SliceableBinaryContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_sliceable

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSliceable" ):
                listener.enterSliceable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSliceable" ):
                listener.exitSliceable(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSliceable" ):
                return visitor.visitSliceable(self)
            else:
                return visitor.visitChildren(self)




    def sliceable(self):

        localctx = JsltParser.SliceableContext(self, self._ctx, self.state)
        self.enterRule(localctx, 62, self.RULE_sliceable)
        try:
            self.state = 301
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,38,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 297
                self.signedNumber()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 298
                self.sliceableLeft()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 299
                self.sliceableRight()
                pass

            elif la_ == 4:
                self.enterOuterAlt(localctx, 4)
                self.state = 300
                self.sliceableBinary()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SignedNumberContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SIGNED_NUMBER(self):
            return self.getToken(JsltParser.SIGNED_NUMBER, 0)

        def NUMBER(self):
            return self.getToken(JsltParser.NUMBER, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_signedNumber

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSignedNumber" ):
                listener.enterSignedNumber(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSignedNumber" ):
                listener.exitSignedNumber(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSignedNumber" ):
                return visitor.visitSignedNumber(self)
            else:
                return visitor.visitChildren(self)




    def signedNumber(self):

        localctx = JsltParser.SignedNumberContext(self, self._ctx, self.state)
        self.enterRule(localctx, 64, self.RULE_signedNumber)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 303
            _la = self._input.LA(1)
            if not(_la==55 or _la==56):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SignedIntContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SIGNED_INT(self):
            return self.getToken(JsltParser.SIGNED_INT, 0)

        def INT(self):
            return self.getToken(JsltParser.INT, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_signedInt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSignedInt" ):
                listener.enterSignedInt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSignedInt" ):
                listener.exitSignedInt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSignedInt" ):
                return visitor.visitSignedInt(self)
            else:
                return visitor.visitChildren(self)




    def signedInt(self):

        localctx = JsltParser.SignedIntContext(self, self._ctx, self.state)
        self.enterRule(localctx, 66, self.RULE_signedInt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 305
            _la = self._input.LA(1)
            if not(_la==57 or _la==58):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SliceableLeftContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def signedNumber(self):
            return self.getTypedRuleContext(JsltParser.SignedNumberContext,0)


        def COLON(self):
            return self.getToken(JsltParser.COLON, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_sliceableLeft

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSliceableLeft" ):
                listener.enterSliceableLeft(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSliceableLeft" ):
                listener.exitSliceableLeft(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSliceableLeft" ):
                return visitor.visitSliceableLeft(self)
            else:
                return visitor.visitChildren(self)




    def sliceableLeft(self):

        localctx = JsltParser.SliceableLeftContext(self, self._ctx, self.state)
        self.enterRule(localctx, 68, self.RULE_sliceableLeft)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 307
            self.signedNumber()
            self.state = 308
            self.match(JsltParser.COLON)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SliceableRightContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def COLON(self):
            return self.getToken(JsltParser.COLON, 0)

        def signedNumber(self):
            return self.getTypedRuleContext(JsltParser.SignedNumberContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_sliceableRight

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSliceableRight" ):
                listener.enterSliceableRight(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSliceableRight" ):
                listener.exitSliceableRight(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSliceableRight" ):
                return visitor.visitSliceableRight(self)
            else:
                return visitor.visitChildren(self)




    def sliceableRight(self):

        localctx = JsltParser.SliceableRightContext(self, self._ctx, self.state)
        self.enterRule(localctx, 70, self.RULE_sliceableRight)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 310
            self.match(JsltParser.COLON)
            self.state = 311
            self.signedNumber()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SliceableBinaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def signedNumber(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JsltParser.SignedNumberContext)
            else:
                return self.getTypedRuleContext(JsltParser.SignedNumberContext,i)


        def COLON(self):
            return self.getToken(JsltParser.COLON, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_sliceableBinary

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSliceableBinary" ):
                listener.enterSliceableBinary(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSliceableBinary" ):
                listener.exitSliceableBinary(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSliceableBinary" ):
                return visitor.visitSliceableBinary(self)
            else:
                return visitor.visitChildren(self)




    def sliceableBinary(self):

        localctx = JsltParser.SliceableBinaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 72, self.RULE_sliceableBinary)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 313
            self.signedNumber()
            self.state = 314
            self.match(JsltParser.COLON)
            self.state = 315
            self.signedNumber()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionsContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JsltParser.ExpressionContext)
            else:
                return self.getTypedRuleContext(JsltParser.ExpressionContext,i)


        def NT(self):
            return self.getToken(JsltParser.NT, 0)

        def binaryOperator(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(JsltParser.BinaryOperatorContext)
            else:
                return self.getTypedRuleContext(JsltParser.BinaryOperatorContext,i)


        def PAREN_LEFT(self):
            return self.getToken(JsltParser.PAREN_LEFT, 0)

        def PAREN_RIGHT(self):
            return self.getToken(JsltParser.PAREN_RIGHT, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_expressions

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpressions" ):
                listener.enterExpressions(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpressions" ):
                listener.exitExpressions(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpressions" ):
                return visitor.visitExpressions(self)
            else:
                return visitor.visitChildren(self)




    def expressions(self):

        localctx = JsltParser.ExpressionsContext(self, self._ctx, self.state)
        self.enterRule(localctx, 74, self.RULE_expressions)
        self._la = 0 # Token type
        try:
            self.state = 332
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,41,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 318
                self._errHandler.sync(self)
                la_ = self._interp.adaptivePredict(self._input,39,self._ctx)
                if la_ == 1:
                    self.state = 317
                    self.match(JsltParser.NT)


                self.state = 320
                self.expression()
                self.state = 324 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while True:
                    self.state = 321
                    self.binaryOperator()
                    self.state = 322
                    self.expression()
                    self.state = 326 
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if not ((((_la) & ~0x3f) == 0 and ((1 << _la) & 207217459200) != 0)):
                        break

                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 328
                self.match(JsltParser.PAREN_LEFT)
                self.state = 329
                self.expression()
                self.state = 330
                self.match(JsltParser.PAREN_RIGHT)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def jsonpath__(self):
            return self.getTypedRuleContext(JsltParser.Jsonpath__Context,0)


        def NT(self):
            return self.getToken(JsltParser.NT, 0)

        def expression(self):
            return self.getTypedRuleContext(JsltParser.ExpressionContext,0)


        def PAREN_LEFT(self):
            return self.getToken(JsltParser.PAREN_LEFT, 0)

        def PAREN_RIGHT(self):
            return self.getToken(JsltParser.PAREN_RIGHT, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpression" ):
                listener.enterExpression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpression" ):
                listener.exitExpression(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpression" ):
                return visitor.visitExpression(self)
            else:
                return visitor.visitChildren(self)




    def expression(self):

        localctx = JsltParser.ExpressionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 76, self.RULE_expression)
        try:
            self.state = 341
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3, 21, 22, 42, 43, 45, 50, 52, 55, 56, 61, 62]:
                self.enterOuterAlt(localctx, 1)
                self.state = 334
                self.jsonpath__()
                pass
            elif token in [30]:
                self.enterOuterAlt(localctx, 2)
                self.state = 335
                self.match(JsltParser.NT)
                self.state = 336
                self.expression()
                pass
            elif token in [48]:
                self.enterOuterAlt(localctx, 3)
                self.state = 337
                self.match(JsltParser.PAREN_LEFT)
                self.state = 338
                self.expression()
                self.state = 339
                self.match(JsltParser.PAREN_RIGHT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BinaryOperatorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def AND(self):
            return self.getToken(JsltParser.AND, 0)

        def OR(self):
            return self.getToken(JsltParser.OR, 0)

        def EQ(self):
            return self.getToken(JsltParser.EQ, 0)

        def NE(self):
            return self.getToken(JsltParser.NE, 0)

        def LT(self):
            return self.getToken(JsltParser.LT, 0)

        def LE(self):
            return self.getToken(JsltParser.LE, 0)

        def GT(self):
            return self.getToken(JsltParser.GT, 0)

        def GE(self):
            return self.getToken(JsltParser.GE, 0)

        def IN(self):
            return self.getToken(JsltParser.IN, 0)

        def NIN(self):
            return self.getToken(JsltParser.NIN, 0)

        def SUBSETOF(self):
            return self.getToken(JsltParser.SUBSETOF, 0)

        def CONTAINS(self):
            return self.getToken(JsltParser.CONTAINS, 0)

        def SIZE(self):
            return self.getToken(JsltParser.SIZE, 0)

        def EMPTY(self):
            return self.getToken(JsltParser.EMPTY, 0)

        def getRuleIndex(self):
            return JsltParser.RULE_binaryOperator

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBinaryOperator" ):
                listener.enterBinaryOperator(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBinaryOperator" ):
                listener.exitBinaryOperator(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBinaryOperator" ):
                return visitor.visitBinaryOperator(self)
            else:
                return visitor.visitChildren(self)




    def binaryOperator(self):

        localctx = JsltParser.BinaryOperatorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 78, self.RULE_binaryOperator)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 343
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 207217459200) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValueContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def STRING(self):
            return self.getToken(JsltParser.STRING, 0)

        def IDQUOTED(self):
            return self.getToken(JsltParser.IDQUOTED, 0)

        def signedNumber(self):
            return self.getTypedRuleContext(JsltParser.SignedNumberContext,0)


        def TRUE(self):
            return self.getToken(JsltParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(JsltParser.FALSE, 0)

        def NULL(self):
            return self.getToken(JsltParser.NULL, 0)

        def obj(self):
            return self.getTypedRuleContext(JsltParser.ObjContext,0)


        def array(self):
            return self.getTypedRuleContext(JsltParser.ArrayContext,0)


        def variable(self):
            return self.getTypedRuleContext(JsltParser.VariableContext,0)


        def getRuleIndex(self):
            return JsltParser.RULE_value

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValue" ):
                listener.enterValue(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValue" ):
                listener.exitValue(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitValue" ):
                return visitor.visitValue(self)
            else:
                return visitor.visitChildren(self)




    def value(self):

        localctx = JsltParser.ValueContext(self, self._ctx, self.state)
        self.enterRule(localctx, 80, self.RULE_value)
        try:
            self.state = 354
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [52]:
                self.enterOuterAlt(localctx, 1)
                self.state = 345
                self.match(JsltParser.STRING)
                pass
            elif token in [61]:
                self.enterOuterAlt(localctx, 2)
                self.state = 346
                self.match(JsltParser.IDQUOTED)
                pass
            elif token in [55, 56]:
                self.enterOuterAlt(localctx, 3)
                self.state = 347
                self.signedNumber()
                pass
            elif token in [21]:
                self.enterOuterAlt(localctx, 4)
                self.state = 348
                self.match(JsltParser.TRUE)
                pass
            elif token in [22]:
                self.enterOuterAlt(localctx, 5)
                self.state = 349
                self.match(JsltParser.FALSE)
                pass
            elif token in [42]:
                self.enterOuterAlt(localctx, 6)
                self.state = 350
                self.match(JsltParser.NULL)
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 7)
                self.state = 351
                self.obj()
                pass
            elif token in [45]:
                self.enterOuterAlt(localctx, 8)
                self.state = 352
                self.array()
                pass
            elif token in [62]:
                self.enterOuterAlt(localctx, 9)
                self.state = 353
                self.variable()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





