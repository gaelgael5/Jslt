# Generated from /home/user/Jslt/grammar/JsltParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JsltParser import JsltParser
else:
    from JsltParser import JsltParser

# This class defines a complete listener for a parse tree produced by JsltParser.
class JsltParserListener(ParseTreeListener):

    # Enter a parse tree produced by JsltParser#script.
    def enterScript(self, ctx:JsltParser.ScriptContext):
        pass

    # Exit a parse tree produced by JsltParser#script.
    def exitScript(self, ctx:JsltParser.ScriptContext):
        pass


    # Enter a parse tree produced by JsltParser#json.
    def enterJson(self, ctx:JsltParser.JsonContext):
        pass

    # Exit a parse tree produced by JsltParser#json.
    def exitJson(self, ctx:JsltParser.JsonContext):
        pass


    # Enter a parse tree produced by JsltParser#obj.
    def enterObj(self, ctx:JsltParser.ObjContext):
        pass

    # Exit a parse tree produced by JsltParser#obj.
    def exitObj(self, ctx:JsltParser.ObjContext):
        pass


    # Enter a parse tree produced by JsltParser#pair.
    def enterPair(self, ctx:JsltParser.PairContext):
        pass

    # Exit a parse tree produced by JsltParser#pair.
    def exitPair(self, ctx:JsltParser.PairContext):
        pass


    # Enter a parse tree produced by JsltParser#string.
    def enterString(self, ctx:JsltParser.StringContext):
        pass

    # Exit a parse tree produced by JsltParser#string.
    def exitString(self, ctx:JsltParser.StringContext):
        pass


    # Enter a parse tree produced by JsltParser#array.
    def enterArray(self, ctx:JsltParser.ArrayContext):
        pass

    # Exit a parse tree produced by JsltParser#array.
    def exitArray(self, ctx:JsltParser.ArrayContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonValue.
    def enterJsonValue(self, ctx:JsltParser.JsonValueContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonValue.
    def exitJsonValue(self, ctx:JsltParser.JsonValueContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonValueString.
    def enterJsonValueString(self, ctx:JsltParser.JsonValueStringContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonValueString.
    def exitJsonValueString(self, ctx:JsltParser.JsonValueStringContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonValueNumber.
    def enterJsonValueNumber(self, ctx:JsltParser.JsonValueNumberContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonValueNumber.
    def exitJsonValueNumber(self, ctx:JsltParser.JsonValueNumberContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonValueInteger.
    def enterJsonValueInteger(self, ctx:JsltParser.JsonValueIntegerContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonValueInteger.
    def exitJsonValueInteger(self, ctx:JsltParser.JsonValueIntegerContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonValueBoolean.
    def enterJsonValueBoolean(self, ctx:JsltParser.JsonValueBooleanContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonValueBoolean.
    def exitJsonValueBoolean(self, ctx:JsltParser.JsonValueBooleanContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonValueNull.
    def enterJsonValueNull(self, ctx:JsltParser.JsonValueNullContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonValueNull.
    def exitJsonValueNull(self, ctx:JsltParser.JsonValueNullContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonType.
    def enterJsonType(self, ctx:JsltParser.JsonTypeContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonType.
    def exitJsonType(self, ctx:JsltParser.JsonTypeContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonLtOperations.
    def enterJsonLtOperations(self, ctx:JsltParser.JsonLtOperationsContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonLtOperations.
    def exitJsonLtOperations(self, ctx:JsltParser.JsonLtOperationsContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonLtOperation.
    def enterJsonLtOperation(self, ctx:JsltParser.JsonLtOperationContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonLtOperation.
    def exitJsonLtOperation(self, ctx:JsltParser.JsonLtOperationContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonLtItem.
    def enterJsonLtItem(self, ctx:JsltParser.JsonLtItemContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonLtItem.
    def exitJsonLtItem(self, ctx:JsltParser.JsonLtItemContext):
        pass


    # Enter a parse tree produced by JsltParser#operation.
    def enterOperation(self, ctx:JsltParser.OperationContext):
        pass

    # Exit a parse tree produced by JsltParser#operation.
    def exitOperation(self, ctx:JsltParser.OperationContext):
        pass


    # Enter a parse tree produced by JsltParser#variable.
    def enterVariable(self, ctx:JsltParser.VariableContext):
        pass

    # Exit a parse tree produced by JsltParser#variable.
    def exitVariable(self, ctx:JsltParser.VariableContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonfunctionCall.
    def enterJsonfunctionCall(self, ctx:JsltParser.JsonfunctionCallContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonfunctionCall.
    def exitJsonfunctionCall(self, ctx:JsltParser.JsonfunctionCallContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonfunctionName.
    def enterJsonfunctionName(self, ctx:JsltParser.JsonfunctionNameContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonfunctionName.
    def exitJsonfunctionName(self, ctx:JsltParser.JsonfunctionNameContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonValueList.
    def enterJsonValueList(self, ctx:JsltParser.JsonValueListContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonValueList.
    def exitJsonValueList(self, ctx:JsltParser.JsonValueListContext):
        pass


    # Enter a parse tree produced by JsltParser#jsltJsonpath.
    def enterJsltJsonpath(self, ctx:JsltParser.JsltJsonpathContext):
        pass

    # Exit a parse tree produced by JsltParser#jsltJsonpath.
    def exitJsltJsonpath(self, ctx:JsltParser.JsltJsonpathContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonpath.
    def enterJsonpath(self, ctx:JsltParser.JsonpathContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonpath.
    def exitJsonpath(self, ctx:JsltParser.JsonpathContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonpath_.
    def enterJsonpath_(self, ctx:JsltParser.Jsonpath_Context):
        pass

    # Exit a parse tree produced by JsltParser#jsonpath_.
    def exitJsonpath_(self, ctx:JsltParser.Jsonpath_Context):
        pass


    # Enter a parse tree produced by JsltParser#jsonpath__.
    def enterJsonpath__(self, ctx:JsltParser.Jsonpath__Context):
        pass

    # Exit a parse tree produced by JsltParser#jsonpath__.
    def exitJsonpath__(self, ctx:JsltParser.Jsonpath__Context):
        pass


    # Enter a parse tree produced by JsltParser#jsonpath_subscript.
    def enterJsonpath_subscript(self, ctx:JsltParser.Jsonpath_subscriptContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonpath_subscript.
    def exitJsonpath_subscript(self, ctx:JsltParser.Jsonpath_subscriptContext):
        pass


    # Enter a parse tree produced by JsltParser#subscriptables.
    def enterSubscriptables(self, ctx:JsltParser.SubscriptablesContext):
        pass

    # Exit a parse tree produced by JsltParser#subscriptables.
    def exitSubscriptables(self, ctx:JsltParser.SubscriptablesContext):
        pass


    # Enter a parse tree produced by JsltParser#subscriptableArguments.
    def enterSubscriptableArguments(self, ctx:JsltParser.SubscriptableArgumentsContext):
        pass

    # Exit a parse tree produced by JsltParser#subscriptableArguments.
    def exitSubscriptableArguments(self, ctx:JsltParser.SubscriptableArgumentsContext):
        pass


    # Enter a parse tree produced by JsltParser#subscriptableBareword.
    def enterSubscriptableBareword(self, ctx:JsltParser.SubscriptableBarewordContext):
        pass

    # Exit a parse tree produced by JsltParser#subscriptableBareword.
    def exitSubscriptableBareword(self, ctx:JsltParser.SubscriptableBarewordContext):
        pass


    # Enter a parse tree produced by JsltParser#jsonPath_identifier.
    def enterJsonPath_identifier(self, ctx:JsltParser.JsonPath_identifierContext):
        pass

    # Exit a parse tree produced by JsltParser#jsonPath_identifier.
    def exitJsonPath_identifier(self, ctx:JsltParser.JsonPath_identifierContext):
        pass


    # Enter a parse tree produced by JsltParser#subscriptable.
    def enterSubscriptable(self, ctx:JsltParser.SubscriptableContext):
        pass

    # Exit a parse tree produced by JsltParser#subscriptable.
    def exitSubscriptable(self, ctx:JsltParser.SubscriptableContext):
        pass


    # Enter a parse tree produced by JsltParser#sliceable.
    def enterSliceable(self, ctx:JsltParser.SliceableContext):
        pass

    # Exit a parse tree produced by JsltParser#sliceable.
    def exitSliceable(self, ctx:JsltParser.SliceableContext):
        pass


    # Enter a parse tree produced by JsltParser#signedNumber.
    def enterSignedNumber(self, ctx:JsltParser.SignedNumberContext):
        pass

    # Exit a parse tree produced by JsltParser#signedNumber.
    def exitSignedNumber(self, ctx:JsltParser.SignedNumberContext):
        pass


    # Enter a parse tree produced by JsltParser#signedInt.
    def enterSignedInt(self, ctx:JsltParser.SignedIntContext):
        pass

    # Exit a parse tree produced by JsltParser#signedInt.
    def exitSignedInt(self, ctx:JsltParser.SignedIntContext):
        pass


    # Enter a parse tree produced by JsltParser#sliceableLeft.
    def enterSliceableLeft(self, ctx:JsltParser.SliceableLeftContext):
        pass

    # Exit a parse tree produced by JsltParser#sliceableLeft.
    def exitSliceableLeft(self, ctx:JsltParser.SliceableLeftContext):
        pass


    # Enter a parse tree produced by JsltParser#sliceableRight.
    def enterSliceableRight(self, ctx:JsltParser.SliceableRightContext):
        pass

    # Exit a parse tree produced by JsltParser#sliceableRight.
    def exitSliceableRight(self, ctx:JsltParser.SliceableRightContext):
        pass


    # Enter a parse tree produced by JsltParser#sliceableBinary.
    def enterSliceableBinary(self, ctx:JsltParser.SliceableBinaryContext):
        pass

    # Exit a parse tree produced by JsltParser#sliceableBinary.
    def exitSliceableBinary(self, ctx:JsltParser.SliceableBinaryContext):
        pass


    # Enter a parse tree produced by JsltParser#expressions.
    def enterExpressions(self, ctx:JsltParser.ExpressionsContext):
        pass

    # Exit a parse tree produced by JsltParser#expressions.
    def exitExpressions(self, ctx:JsltParser.ExpressionsContext):
        pass


    # Enter a parse tree produced by JsltParser#expression.
    def enterExpression(self, ctx:JsltParser.ExpressionContext):
        pass

    # Exit a parse tree produced by JsltParser#expression.
    def exitExpression(self, ctx:JsltParser.ExpressionContext):
        pass


    # Enter a parse tree produced by JsltParser#binaryOperator.
    def enterBinaryOperator(self, ctx:JsltParser.BinaryOperatorContext):
        pass

    # Exit a parse tree produced by JsltParser#binaryOperator.
    def exitBinaryOperator(self, ctx:JsltParser.BinaryOperatorContext):
        pass


    # Enter a parse tree produced by JsltParser#value.
    def enterValue(self, ctx:JsltParser.ValueContext):
        pass

    # Exit a parse tree produced by JsltParser#value.
    def exitValue(self, ctx:JsltParser.ValueContext):
        pass



del JsltParser