# Generated from /home/user/Jslt/grammar/JsltParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .JsltParser import JsltParser
else:
    from JsltParser import JsltParser

# This class defines a complete generic visitor for a parse tree produced by JsltParser.

class JsltParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by JsltParser#script.
    def visitScript(self, ctx:JsltParser.ScriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#json.
    def visitJson(self, ctx:JsltParser.JsonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#obj.
    def visitObj(self, ctx:JsltParser.ObjContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#pair.
    def visitPair(self, ctx:JsltParser.PairContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#string.
    def visitString(self, ctx:JsltParser.StringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#array.
    def visitArray(self, ctx:JsltParser.ArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonValue.
    def visitJsonValue(self, ctx:JsltParser.JsonValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonValueString.
    def visitJsonValueString(self, ctx:JsltParser.JsonValueStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonValueNumber.
    def visitJsonValueNumber(self, ctx:JsltParser.JsonValueNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonValueInteger.
    def visitJsonValueInteger(self, ctx:JsltParser.JsonValueIntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonValueBoolean.
    def visitJsonValueBoolean(self, ctx:JsltParser.JsonValueBooleanContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonValueNull.
    def visitJsonValueNull(self, ctx:JsltParser.JsonValueNullContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonType.
    def visitJsonType(self, ctx:JsltParser.JsonTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonLtOperations.
    def visitJsonLtOperations(self, ctx:JsltParser.JsonLtOperationsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonLtOperation.
    def visitJsonLtOperation(self, ctx:JsltParser.JsonLtOperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonLtItem.
    def visitJsonLtItem(self, ctx:JsltParser.JsonLtItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#operation.
    def visitOperation(self, ctx:JsltParser.OperationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#variable.
    def visitVariable(self, ctx:JsltParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonfunctionCall.
    def visitJsonfunctionCall(self, ctx:JsltParser.JsonfunctionCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonfunctionName.
    def visitJsonfunctionName(self, ctx:JsltParser.JsonfunctionNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonValueList.
    def visitJsonValueList(self, ctx:JsltParser.JsonValueListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsltJsonpath.
    def visitJsltJsonpath(self, ctx:JsltParser.JsltJsonpathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonpath.
    def visitJsonpath(self, ctx:JsltParser.JsonpathContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonpath_.
    def visitJsonpath_(self, ctx:JsltParser.Jsonpath_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonpath__.
    def visitJsonpath__(self, ctx:JsltParser.Jsonpath__Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonpath_subscript.
    def visitJsonpath_subscript(self, ctx:JsltParser.Jsonpath_subscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#subscriptables.
    def visitSubscriptables(self, ctx:JsltParser.SubscriptablesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#subscriptableArguments.
    def visitSubscriptableArguments(self, ctx:JsltParser.SubscriptableArgumentsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#subscriptableBareword.
    def visitSubscriptableBareword(self, ctx:JsltParser.SubscriptableBarewordContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#jsonPath_identifier.
    def visitJsonPath_identifier(self, ctx:JsltParser.JsonPath_identifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#subscriptable.
    def visitSubscriptable(self, ctx:JsltParser.SubscriptableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#sliceable.
    def visitSliceable(self, ctx:JsltParser.SliceableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#signedNumber.
    def visitSignedNumber(self, ctx:JsltParser.SignedNumberContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#signedInt.
    def visitSignedInt(self, ctx:JsltParser.SignedIntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#sliceableLeft.
    def visitSliceableLeft(self, ctx:JsltParser.SliceableLeftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#sliceableRight.
    def visitSliceableRight(self, ctx:JsltParser.SliceableRightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#sliceableBinary.
    def visitSliceableBinary(self, ctx:JsltParser.SliceableBinaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#expressions.
    def visitExpressions(self, ctx:JsltParser.ExpressionsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#expression.
    def visitExpression(self, ctx:JsltParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#binaryOperator.
    def visitBinaryOperator(self, ctx:JsltParser.BinaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by JsltParser#value.
    def visitValue(self, ctx:JsltParser.ValueContext):
        return self.visitChildren(ctx)



del JsltParser