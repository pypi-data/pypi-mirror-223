/* eslint-disable */
;(function(root, factory) {
  if (typeof define === 'function' && define.amd) { // AMD
    define([], factory);
  } else if (typeof exports === 'object') { // Node.js
    module.exports = factory();
  } else { // Browser
    var messages = factory();
    for (var key in messages) {
      root.Blockly.Msg[key] = messages[key];
    }
  }
}(this, function() {
// This file was automatically generated.  Do not modify.

'use strict';

var Blockly = Blockly || { Msg: Object.create(null) };

Blockly.Msg["ADD_COMMENT"] = "Bemierkung derbäisetzen";
Blockly.Msg["CANNOT_DELETE_VARIABLE_PROCEDURE"] = "Can't delete the variable '%1' because it's part of the definition of the function '%2'";  // untranslated
Blockly.Msg["CHANGE_VALUE_TITLE"] = "Wäert änneren:";
Blockly.Msg["CLEAN_UP"] = "Bléck opraumen";
Blockly.Msg["COLLAPSED_WARNINGS_WARNING"] = "Collapsed blocks contain warnings.";  // untranslated
Blockly.Msg["COLLAPSE_ALL"] = "Bléck zesummeklappen";
Blockly.Msg["COLLAPSE_BLOCK"] = "Block zesummeklappen";
Blockly.Msg["COLOUR_BLEND_COLOUR1"] = "Faarf 1";
Blockly.Msg["COLOUR_BLEND_COLOUR2"] = "Faarf 2";
Blockly.Msg["COLOUR_BLEND_HELPURL"] = "https://meyerweb.com/eric/tools/color-blend/#:::rgbp";  // untranslated
Blockly.Msg["COLOUR_BLEND_RATIO"] = "ratio";
Blockly.Msg["COLOUR_BLEND_TITLE"] = "mëschen";
Blockly.Msg["COLOUR_BLEND_TOOLTIP"] = "Blends two colours together with a given ratio (0.0 - 1.0).";  // untranslated
Blockly.Msg["COLOUR_PICKER_HELPURL"] = "https://en.wikipedia.org/wiki/Color";  // untranslated
Blockly.Msg["COLOUR_PICKER_TOOLTIP"] = "Sicht eng Faarf an der Palette eraus.";
Blockly.Msg["COLOUR_RANDOM_HELPURL"] = "http://randomcolour.com";  // untranslated
Blockly.Msg["COLOUR_RANDOM_TITLE"] = "zoufälleg Faarf";
Blockly.Msg["COLOUR_RANDOM_TOOLTIP"] = "Eng zoufälleg Faarf eraussichen.";
Blockly.Msg["COLOUR_RGB_BLUE"] = "blo";
Blockly.Msg["COLOUR_RGB_GREEN"] = "gréng";
Blockly.Msg["COLOUR_RGB_HELPURL"] = "https://www.december.com/html/spec/colorpercompact.html";  // untranslated
Blockly.Msg["COLOUR_RGB_RED"] = "rout";
Blockly.Msg["COLOUR_RGB_TITLE"] = "fierwe mat";
Blockly.Msg["COLOUR_RGB_TOOLTIP"] = "Create a colour with the specified amount of red, green, and blue. All values must be between 0 and 100.";  // untranslated
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#loop-termination-blocks";  // untranslated
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_OPERATOR_BREAK"] = "break out of loop";  // untranslated
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_OPERATOR_CONTINUE"] = "continue with next iteration of loop";  // untranslated
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_TOOLTIP_BREAK"] = "Break out of the containing loop.";  // untranslated
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_TOOLTIP_CONTINUE"] = "Skip the rest of this loop, and continue with the next iteration.";  // untranslated
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_WARNING"] = "Warning: This block may only be used within a loop.";  // untranslated
Blockly.Msg["CONTROLS_FOREACH_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#for-each";  // untranslated
Blockly.Msg["CONTROLS_FOREACH_TITLE"] = "fir all Element %1 an der Lëscht %2";
Blockly.Msg["CONTROLS_FOREACH_TOOLTIP"] = "For each item in a list, set the variable '%1' to the item, and then do some statements.";  // untranslated
Blockly.Msg["CONTROLS_FOR_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#count-with";  // untranslated
Blockly.Msg["CONTROLS_FOR_TITLE"] = "zielt mat %1 vun %2 bis %3 mat %4";
Blockly.Msg["CONTROLS_FOR_TOOLTIP"] = "Have the variable '%1' take on the values from the start number to the end number, counting by the specified interval, and do the specified blocks.";  // untranslated
Blockly.Msg["CONTROLS_IF_ELSEIF_TOOLTIP"] = "Add a condition to the if block.";  // untranslated
Blockly.Msg["CONTROLS_IF_ELSE_TOOLTIP"] = "Add a final, catch-all condition to the if block.";  // untranslated
Blockly.Msg["CONTROLS_IF_HELPURL"] = "https://github.com/google/blockly/wiki/IfElse";  // untranslated
Blockly.Msg["CONTROLS_IF_IF_TOOLTIP"] = "Add, remove, or reorder sections to reconfigure this if block.";  // untranslated
Blockly.Msg["CONTROLS_IF_MSG_ELSE"] = "soss";
Blockly.Msg["CONTROLS_IF_MSG_ELSEIF"] = "else if";  // untranslated
Blockly.Msg["CONTROLS_IF_MSG_IF"] = "wann";
Blockly.Msg["CONTROLS_IF_TOOLTIP_1"] = "If a value is true, then do some statements.";  // untranslated
Blockly.Msg["CONTROLS_IF_TOOLTIP_2"] = "If a value is true, then do the first block of statements. Otherwise, do the second block of statements.";  // untranslated
Blockly.Msg["CONTROLS_IF_TOOLTIP_3"] = "If the first value is true, then do the first block of statements. Otherwise, if the second value is true, do the second block of statements.";  // untranslated
Blockly.Msg["CONTROLS_IF_TOOLTIP_4"] = "If the first value is true, then do the first block of statements. Otherwise, if the second value is true, do the second block of statements. If none of the values are true, do the last block of statements.";  // untranslated
Blockly.Msg["CONTROLS_REPEAT_HELPURL"] = "https://en.wikipedia.org/wiki/For_loop";  // untranslated
Blockly.Msg["CONTROLS_REPEAT_INPUT_DO"] = "maach";
Blockly.Msg["CONTROLS_REPEAT_TITLE"] = "%1-mol widderhuelen";
Blockly.Msg["CONTROLS_REPEAT_TOOLTIP"] = "Do some statements several times.";  // untranslated
Blockly.Msg["CONTROLS_WHILEUNTIL_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#repeat";  // untranslated
Blockly.Msg["CONTROLS_WHILEUNTIL_OPERATOR_UNTIL"] = "widderhuele bis";
Blockly.Msg["CONTROLS_WHILEUNTIL_OPERATOR_WHILE"] = "Widderhuel soulaang";
Blockly.Msg["CONTROLS_WHILEUNTIL_TOOLTIP_UNTIL"] = "Féiert d'Uweisungen aus, soulaang wéi de Wäert falsch ass.";
Blockly.Msg["CONTROLS_WHILEUNTIL_TOOLTIP_WHILE"] = "Féiert d'Uweisungen aus, soulaang wéi de Wäert richteg ass";
Blockly.Msg["DELETE_ALL_BLOCKS"] = "Delete all %1 blocks?";  // untranslated
Blockly.Msg["DELETE_BLOCK"] = "Block läschen";
Blockly.Msg["DELETE_VARIABLE"] = "Delete the '%1' variable";  // untranslated
Blockly.Msg["DELETE_VARIABLE_CONFIRMATION"] = "Delete %1 uses of the '%2' variable?";  // untranslated
Blockly.Msg["DELETE_X_BLOCKS"] = "%1 Bléck läschen";
Blockly.Msg["DIALOG_CANCEL"] = "Ofbriechen";
Blockly.Msg["DIALOG_OK"] = "OK";
Blockly.Msg["DISABLE_BLOCK"] = "Block desaktivéieren";
Blockly.Msg["DUPLICATE_BLOCK"] = "Eng Kopie maachen";
Blockly.Msg["DUPLICATE_COMMENT"] = "Bemierkung kopéieren";
Blockly.Msg["ENABLE_BLOCK"] = "Block aktivéieren";
Blockly.Msg["EXPAND_ALL"] = "Bléck opklappen";
Blockly.Msg["EXPAND_BLOCK"] = "Block opklappen";
Blockly.Msg["EXTERNAL_INPUTS"] = "External Inputs";  // untranslated
Blockly.Msg["HELP"] = "Hëllef";
Blockly.Msg["INLINE_INPUTS"] = "Inline Inputs";  // untranslated
Blockly.Msg["LISTS_CREATE_EMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-empty-list";  // untranslated
Blockly.Msg["LISTS_CREATE_EMPTY_TITLE"] = "create empty list";  // untranslated
Blockly.Msg["LISTS_CREATE_EMPTY_TOOLTIP"] = "Returns a list, of length 0, containing no data records";  // untranslated
Blockly.Msg["LISTS_CREATE_WITH_CONTAINER_TITLE_ADD"] = "Lëscht";
Blockly.Msg["LISTS_CREATE_WITH_CONTAINER_TOOLTIP"] = "Add, remove, or reorder sections to reconfigure this list block.";  // untranslated
Blockly.Msg["LISTS_CREATE_WITH_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-list-with";  // untranslated
Blockly.Msg["LISTS_CREATE_WITH_INPUT_WITH"] = "create list with";  // untranslated
Blockly.Msg["LISTS_CREATE_WITH_ITEM_TOOLTIP"] = "En Element op d'Lëscht derbäisetzen.";
Blockly.Msg["LISTS_CREATE_WITH_TOOLTIP"] = "Create a list with any number of items.";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_FIRST"] = "éischt";
Blockly.Msg["LISTS_GET_INDEX_FROM_END"] = "# vun hannen";
Blockly.Msg["LISTS_GET_INDEX_FROM_START"] = "#";
Blockly.Msg["LISTS_GET_INDEX_GET"] = "get";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_GET_REMOVE"] = "get and remove";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_LAST"] = "lescht";
Blockly.Msg["LISTS_GET_INDEX_RANDOM"] = "Zoufall";
Blockly.Msg["LISTS_GET_INDEX_REMOVE"] = "ewechhuelen";
Blockly.Msg["LISTS_GET_INDEX_TAIL"] = "";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_FIRST"] = "Returns the first item in a list.";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_FROM"] = "Returns the item at the specified position in a list.";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_LAST"] = "Returns the last item in a list.";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_RANDOM"] = "Schéckt en zoufällegt Element aus enger Lëscht zréck.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_FIRST"] = "Removes and returns the first item in a list.";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_FROM"] = "Removes and returns the item at the specified position in a list.";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_LAST"] = "Removes and returns the last item in a list.";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_RANDOM"] = "Removes and returns a random item in a list.";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_FIRST"] = "Removes the first item in a list.";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_FROM"] = "Removes the item at the specified position in a list.";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_LAST"] = "Hëlt dat lescht Element aus enger Lëscht eraus.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_RANDOM"] = "Hëlt en zoufällegt Element aus enger Lëscht eraus.";
Blockly.Msg["LISTS_GET_SUBLIST_END_FROM_END"] = "to # from end";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_END_FROM_START"] = "to #";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_END_LAST"] = "to last";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#getting-a-sublist";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_START_FIRST"] = "get sub-list from first";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_START_FROM_END"] = "get sub-list from # from end";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_START_FROM_START"] = "get sub-list from #";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_TAIL"] = "";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_TOOLTIP"] = "Creates a copy of the specified portion of a list.";  // untranslated
Blockly.Msg["LISTS_INDEX_FROM_END_TOOLTIP"] = "%1 ass dat éischt Element.";
Blockly.Msg["LISTS_INDEX_FROM_START_TOOLTIP"] = "%1 ass dat éischt Element.";
Blockly.Msg["LISTS_INDEX_OF_FIRST"] = "find first occurrence of item";  // untranslated
Blockly.Msg["LISTS_INDEX_OF_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#getting-items-from-a-list";  // untranslated
Blockly.Msg["LISTS_INDEX_OF_LAST"] = "find last occurrence of item";  // untranslated
Blockly.Msg["LISTS_INDEX_OF_TOOLTIP"] = "Returns the index of the first/last occurrence of the item in the list. Returns %1 if item is not found.";  // untranslated
Blockly.Msg["LISTS_INLIST"] = "an der Lëscht";
Blockly.Msg["LISTS_ISEMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#is-empty";  // untranslated
Blockly.Msg["LISTS_ISEMPTY_TITLE"] = "%1 ass eidel";
Blockly.Msg["LISTS_ISEMPTY_TOOLTIP"] = "Returns true if the list is empty.";  // untranslated
Blockly.Msg["LISTS_LENGTH_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#length-of";  // untranslated
Blockly.Msg["LISTS_LENGTH_TITLE"] = "Längt vu(n) %1";
Blockly.Msg["LISTS_LENGTH_TOOLTIP"] = "Returns the length of a list.";  // untranslated
Blockly.Msg["LISTS_REPEAT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-list-with";  // untranslated
Blockly.Msg["LISTS_REPEAT_TITLE"] = "create list with item %1 repeated %2 times";  // untranslated
Blockly.Msg["LISTS_REPEAT_TOOLTIP"] = "Creates a list consisting of the given value repeated the specified number of times.";  // untranslated
Blockly.Msg["LISTS_REVERSE_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#reversing-a-list";  // untranslated
Blockly.Msg["LISTS_REVERSE_MESSAGE0"] = "%1 ëmdréinen";
Blockly.Msg["LISTS_REVERSE_TOOLTIP"] = "Reverse a copy of a list.";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#in-list--set";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_INPUT_TO"] = "als";
Blockly.Msg["LISTS_SET_INDEX_INSERT"] = "asetzen op";
Blockly.Msg["LISTS_SET_INDEX_SET"] = "set";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_FIRST"] = "Inserts the item at the start of a list.";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_FROM"] = "Inserts the item at the specified position in a list.";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_LAST"] = "Setzt d'Element um Enn vun enger Lëscht derbäi.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_RANDOM"] = "Setzt d'Element op eng zoufälleg Plaz an d'Lëscht derbäi.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_FIRST"] = "Sets the first item in a list.";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_FROM"] = "Sets the item at the specified position in a list.";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_LAST"] = "Sets the last item in a list.";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_RANDOM"] = "Setzt en zoufällegt Element an eng Lëscht.";
Blockly.Msg["LISTS_SORT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#sorting-a-list";  // untranslated
Blockly.Msg["LISTS_SORT_ORDER_ASCENDING"] = "ascending";  // untranslated
Blockly.Msg["LISTS_SORT_ORDER_DESCENDING"] = "descending";  // untranslated
Blockly.Msg["LISTS_SORT_TITLE"] = "%1 %2 %3 zortéieren";
Blockly.Msg["LISTS_SORT_TOOLTIP"] = "Sort a copy of a list.";  // untranslated
Blockly.Msg["LISTS_SORT_TYPE_IGNORECASE"] = "alphabetic, ignore case";  // untranslated
Blockly.Msg["LISTS_SORT_TYPE_NUMERIC"] = "numeresch";
Blockly.Msg["LISTS_SORT_TYPE_TEXT"] = "alphabetesch";
Blockly.Msg["LISTS_SPLIT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#splitting-strings-and-joining-lists";  // untranslated
Blockly.Msg["LISTS_SPLIT_LIST_FROM_TEXT"] = "make list from text";  // untranslated
Blockly.Msg["LISTS_SPLIT_TEXT_FROM_LIST"] = "make text from list";  // untranslated
Blockly.Msg["LISTS_SPLIT_TOOLTIP_JOIN"] = "Join a list of texts into one text, separated by a delimiter.";  // untranslated
Blockly.Msg["LISTS_SPLIT_TOOLTIP_SPLIT"] = "Split text into a list of texts, breaking at each delimiter.";  // untranslated
Blockly.Msg["LISTS_SPLIT_WITH_DELIMITER"] = "with delimiter";  // untranslated
Blockly.Msg["LOGIC_BOOLEAN_FALSE"] = "falsch";
Blockly.Msg["LOGIC_BOOLEAN_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#values";  // untranslated
Blockly.Msg["LOGIC_BOOLEAN_TOOLTIP"] = "Schéckt entweder richteg oder falsch zréck.";
Blockly.Msg["LOGIC_BOOLEAN_TRUE"] = "wouer";
Blockly.Msg["LOGIC_COMPARE_HELPURL"] = "https://en.wikipedia.org/wiki/Inequality_(mathematics)";  // untranslated
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_EQ"] = "Return true if both inputs equal each other.";  // untranslated
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_GT"] = "Return true if the first input is greater than the second input.";  // untranslated
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_GTE"] = "Return true if the first input is greater than or equal to the second input.";  // untranslated
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_LT"] = "Return true if the first input is smaller than the second input.";  // untranslated
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_LTE"] = "Return true if the first input is smaller than or equal to the second input.";  // untranslated
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_NEQ"] = "Return true if both inputs are not equal to each other.";  // untranslated
Blockly.Msg["LOGIC_NEGATE_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#not";  // untranslated
Blockly.Msg["LOGIC_NEGATE_TITLE"] = "net %1";
Blockly.Msg["LOGIC_NEGATE_TOOLTIP"] = "Returns true if the input is false. Returns false if the input is true.";  // untranslated
Blockly.Msg["LOGIC_NULL"] = "null";
Blockly.Msg["LOGIC_NULL_HELPURL"] = "https://en.wikipedia.org/wiki/Nullable_type";  // untranslated
Blockly.Msg["LOGIC_NULL_TOOLTIP"] = "Returns null.";  // untranslated
Blockly.Msg["LOGIC_OPERATION_AND"] = "an";
Blockly.Msg["LOGIC_OPERATION_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#logical-operations";  // untranslated
Blockly.Msg["LOGIC_OPERATION_OR"] = "oder";
Blockly.Msg["LOGIC_OPERATION_TOOLTIP_AND"] = "Return true if both inputs are true.";  // untranslated
Blockly.Msg["LOGIC_OPERATION_TOOLTIP_OR"] = "Return true if at least one of the inputs is true.";  // untranslated
Blockly.Msg["LOGIC_TERNARY_CONDITION"] = "Test";
Blockly.Msg["LOGIC_TERNARY_HELPURL"] = "https://en.wikipedia.org/wiki/%3F:";  // untranslated
Blockly.Msg["LOGIC_TERNARY_IF_FALSE"] = "wa falsch";
Blockly.Msg["LOGIC_TERNARY_IF_TRUE"] = "wa wouer";
Blockly.Msg["LOGIC_TERNARY_TOOLTIP"] = "Check the condition in 'test'. If the condition is true, returns the 'if true' value; otherwise returns the 'if false' value.";  // untranslated
Blockly.Msg["MATH_ADDITION_SYMBOL"] = "+";  // untranslated
Blockly.Msg["MATH_ARITHMETIC_HELPURL"] = "https://en.wikipedia.org/wiki/Arithmetic";  // untranslated
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_ADD"] = "Den Total vun den zwou Zuelen zréckginn.";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_DIVIDE"] = "Return the quotient of the two numbers.";  // untranslated
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_MINUS"] = "Return the difference of the two numbers.";  // untranslated
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_MULTIPLY"] = "D'Produkt vun den zwou Zuelen zréckginn.";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_POWER"] = "Return the first number raised to the power of the second number.";  // untranslated
Blockly.Msg["MATH_ATAN2_HELPURL"] = "https://en.wikipedia.org/wiki/Atan2";  // untranslated
Blockly.Msg["MATH_ATAN2_TITLE"] = "atan2 of X:%1 Y:%2";  // untranslated
Blockly.Msg["MATH_ATAN2_TOOLTIP"] = "Return the arctangent of point (X, Y) in degrees from -180 to 180.";  // untranslated
Blockly.Msg["MATH_CHANGE_HELPURL"] = "https://en.wikipedia.org/wiki/Programming_idiom#Incrementing_a_counter";  // untranslated
Blockly.Msg["MATH_CHANGE_TITLE"] = "änneren %1 ëm %2";
Blockly.Msg["MATH_CHANGE_TOOLTIP"] = "Add a number to variable '%1'.";  // untranslated
Blockly.Msg["MATH_CONSTANT_HELPURL"] = "https://en.wikipedia.org/wiki/Mathematical_constant";  // untranslated
Blockly.Msg["MATH_CONSTANT_TOOLTIP"] = "Return one of the common constants: π (3.141…), e (2.718…), φ (1.618…), sqrt(2) (1.414…), sqrt(½) (0.707…), or ∞ (infinity).";  // untranslated
Blockly.Msg["MATH_CONSTRAIN_HELPURL"] = "https://en.wikipedia.org/wiki/Clamping_(graphics)";  // untranslated
Blockly.Msg["MATH_CONSTRAIN_TITLE"] = "constrain %1 low %2 high %3";  // untranslated
Blockly.Msg["MATH_CONSTRAIN_TOOLTIP"] = "Constrain a number to be between the specified limits (inclusive).";  // untranslated
Blockly.Msg["MATH_DIVISION_SYMBOL"] = "÷";  // untranslated
Blockly.Msg["MATH_IS_DIVISIBLE_BY"] = "is divisible by";  // untranslated
Blockly.Msg["MATH_IS_EVEN"] = "ass gerued";
Blockly.Msg["MATH_IS_NEGATIVE"] = "ass negativ";
Blockly.Msg["MATH_IS_ODD"] = "ass ongerued";
Blockly.Msg["MATH_IS_POSITIVE"] = "ass positiv";
Blockly.Msg["MATH_IS_PRIME"] = "ass eng Primzuel";
Blockly.Msg["MATH_IS_TOOLTIP"] = "Check if a number is an even, odd, prime, whole, positive, negative, or if it is divisible by certain number. Returns true or false.";  // untranslated
Blockly.Msg["MATH_IS_WHOLE"] = "ass eng ganz Zuel";
Blockly.Msg["MATH_MODULO_HELPURL"] = "https://en.wikipedia.org/wiki/Modulo_operation";  // untranslated
Blockly.Msg["MATH_MODULO_TITLE"] = "Rescht vu(n) %1 ÷ %2";
Blockly.Msg["MATH_MODULO_TOOLTIP"] = "Return the remainder from dividing the two numbers.";  // untranslated
Blockly.Msg["MATH_MULTIPLICATION_SYMBOL"] = "×";  // untranslated
Blockly.Msg["MATH_NUMBER_HELPURL"] = "https://en.wikipedia.org/wiki/Number";  // untranslated
Blockly.Msg["MATH_NUMBER_TOOLTIP"] = "Eng Zuel.";
Blockly.Msg["MATH_ONLIST_HELPURL"] = "";  // untranslated
Blockly.Msg["MATH_ONLIST_OPERATOR_AVERAGE"] = "Moyenne vun der Lëscht";
Blockly.Msg["MATH_ONLIST_OPERATOR_MAX"] = "Maximum aus der Lëscht";
Blockly.Msg["MATH_ONLIST_OPERATOR_MEDIAN"] = "median of list";  // untranslated
Blockly.Msg["MATH_ONLIST_OPERATOR_MIN"] = "min of list";  // untranslated
Blockly.Msg["MATH_ONLIST_OPERATOR_MODE"] = "modes of list";  // untranslated
Blockly.Msg["MATH_ONLIST_OPERATOR_RANDOM"] = "zoufällegt Element vun enger Lëscht";
Blockly.Msg["MATH_ONLIST_OPERATOR_STD_DEV"] = "standard deviation of list";  // untranslated
Blockly.Msg["MATH_ONLIST_OPERATOR_SUM"] = "sum of list";  // untranslated
Blockly.Msg["MATH_ONLIST_TOOLTIP_AVERAGE"] = "Return the average (arithmetic mean) of the numeric values in the list.";  // untranslated
Blockly.Msg["MATH_ONLIST_TOOLTIP_MAX"] = "Schéckt de gréisste Wäert aus enger Lëscht zréck.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MEDIAN"] = "Return the median number in the list.";  // untranslated
Blockly.Msg["MATH_ONLIST_TOOLTIP_MIN"] = "Return the smallest number in the list.";  // untranslated
Blockly.Msg["MATH_ONLIST_TOOLTIP_MODE"] = "Return a list of the most common item(s) in the list.";  // untranslated
Blockly.Msg["MATH_ONLIST_TOOLTIP_RANDOM"] = "Return a random element from the list.";  // untranslated
Blockly.Msg["MATH_ONLIST_TOOLTIP_STD_DEV"] = "Return the standard deviation of the list.";  // untranslated
Blockly.Msg["MATH_ONLIST_TOOLTIP_SUM"] = "Return the sum of all the numbers in the list.";  // untranslated
Blockly.Msg["MATH_POWER_SYMBOL"] = "^";  // untranslated
Blockly.Msg["MATH_RANDOM_FLOAT_HELPURL"] = "https://en.wikipedia.org/wiki/Random_number_generation";  // untranslated
Blockly.Msg["MATH_RANDOM_FLOAT_TITLE_RANDOM"] = "random fraction";  // untranslated
Blockly.Msg["MATH_RANDOM_FLOAT_TOOLTIP"] = "Return a random fraction between 0.0 (inclusive) and 1.0 (exclusive).";  // untranslated
Blockly.Msg["MATH_RANDOM_INT_HELPURL"] = "https://en.wikipedia.org/wiki/Random_number_generation";  // untranslated
Blockly.Msg["MATH_RANDOM_INT_TITLE"] = "zoufälleg ganz Zuel tëscht %1 a(n) %2";
Blockly.Msg["MATH_RANDOM_INT_TOOLTIP"] = "Return a random integer between the two specified limits, inclusive.";  // untranslated
Blockly.Msg["MATH_ROUND_HELPURL"] = "https://en.wikipedia.org/wiki/Rounding";  // untranslated
Blockly.Msg["MATH_ROUND_OPERATOR_ROUND"] = "opronnen";
Blockly.Msg["MATH_ROUND_OPERATOR_ROUNDDOWN"] = "ofrënnen";
Blockly.Msg["MATH_ROUND_OPERATOR_ROUNDUP"] = "oprënnen";
Blockly.Msg["MATH_ROUND_TOOLTIP"] = "Eng Zuel op- oder ofrënnen.";
Blockly.Msg["MATH_SINGLE_HELPURL"] = "https://lb.wikipedia.org/wiki/Racine carrée";
Blockly.Msg["MATH_SINGLE_OP_ABSOLUTE"] = "absolut";
Blockly.Msg["MATH_SINGLE_OP_ROOT"] = "Quadratwuerzel";
Blockly.Msg["MATH_SINGLE_TOOLTIP_ABS"] = "Return the absolute value of a number.";  // untranslated
Blockly.Msg["MATH_SINGLE_TOOLTIP_EXP"] = "Return e to the power of a number.";  // untranslated
Blockly.Msg["MATH_SINGLE_TOOLTIP_LN"] = "Return the natural logarithm of a number.";  // untranslated
Blockly.Msg["MATH_SINGLE_TOOLTIP_LOG10"] = "Return the base 10 logarithm of a number.";  // untranslated
Blockly.Msg["MATH_SINGLE_TOOLTIP_NEG"] = "Return the negation of a number.";  // untranslated
Blockly.Msg["MATH_SINGLE_TOOLTIP_POW10"] = "Return 10 to the power of a number.";  // untranslated
Blockly.Msg["MATH_SINGLE_TOOLTIP_ROOT"] = "Return the square root of a number.";  // untranslated
Blockly.Msg["MATH_SUBTRACTION_SYMBOL"] = "-";  // untranslated
Blockly.Msg["MATH_TRIG_ACOS"] = "acos";  // untranslated
Blockly.Msg["MATH_TRIG_ASIN"] = "asin";  // untranslated
Blockly.Msg["MATH_TRIG_ATAN"] = "atan";  // untranslated
Blockly.Msg["MATH_TRIG_COS"] = "cos";  // untranslated
Blockly.Msg["MATH_TRIG_HELPURL"] = "https://en.wikipedia.org/wiki/Trigonometric_functions";  // untranslated
Blockly.Msg["MATH_TRIG_SIN"] = "sin";  // untranslated
Blockly.Msg["MATH_TRIG_TAN"] = "tan";  // untranslated
Blockly.Msg["MATH_TRIG_TOOLTIP_ACOS"] = "Return the arccosine of a number.";  // untranslated
Blockly.Msg["MATH_TRIG_TOOLTIP_ASIN"] = "Return the arcsine of a number.";  // untranslated
Blockly.Msg["MATH_TRIG_TOOLTIP_ATAN"] = "Return the arctangent of a number.";  // untranslated
Blockly.Msg["MATH_TRIG_TOOLTIP_COS"] = "Return the cosine of a degree (not radian).";  // untranslated
Blockly.Msg["MATH_TRIG_TOOLTIP_SIN"] = "Return the sine of a degree (not radian).";  // untranslated
Blockly.Msg["MATH_TRIG_TOOLTIP_TAN"] = "Return the tangent of a degree (not radian).";  // untranslated
Blockly.Msg["NEW_COLOUR_VARIABLE"] = "Create colour variable...";  // untranslated
Blockly.Msg["NEW_NUMBER_VARIABLE"] = "Create number variable...";  // untranslated
Blockly.Msg["NEW_STRING_VARIABLE"] = "Create string variable...";  // untranslated
Blockly.Msg["NEW_VARIABLE"] = "Variabel uleeën...";
Blockly.Msg["NEW_VARIABLE_TITLE"] = "Neie variabelen Numm:";
Blockly.Msg["NEW_VARIABLE_TYPE_TITLE"] = "New variable type:";  // untranslated
Blockly.Msg["ORDINAL_NUMBER_SUFFIX"] = "";  // untranslated
Blockly.Msg["PROCEDURES_ALLOW_STATEMENTS"] = "allow statements";  // untranslated
Blockly.Msg["PROCEDURES_BEFORE_PARAMS"] = "mat:";
Blockly.Msg["PROCEDURES_CALLNORETURN_HELPURL"] = "https://en.wikipedia.org/wiki/Subroutine";  // untranslated
Blockly.Msg["PROCEDURES_CALLNORETURN_TOOLTIP"] = "Run the user-defined function '%1'.";  // untranslated
Blockly.Msg["PROCEDURES_CALLRETURN_HELPURL"] = "https://en.wikipedia.org/wiki/Subroutine";  // untranslated
Blockly.Msg["PROCEDURES_CALLRETURN_TOOLTIP"] = "Run the user-defined function '%1' and use its output.";  // untranslated
Blockly.Msg["PROCEDURES_CALL_BEFORE_PARAMS"] = "mat:";
Blockly.Msg["PROCEDURES_CREATE_DO"] = "'%1' uleeën";
Blockly.Msg["PROCEDURES_DEFNORETURN_COMMENT"] = "Dës Funktioun beschreiwen...";
Blockly.Msg["PROCEDURES_DEFNORETURN_DO"] = "";  // untranslated
Blockly.Msg["PROCEDURES_DEFNORETURN_HELPURL"] = "https://en.wikipedia.org/wiki/Subroutine";  // untranslated
Blockly.Msg["PROCEDURES_DEFNORETURN_PROCEDURE"] = "eppes maachen";
Blockly.Msg["PROCEDURES_DEFNORETURN_TITLE"] = "to";  // untranslated
Blockly.Msg["PROCEDURES_DEFNORETURN_TOOLTIP"] = "Creates a function with no output.";  // untranslated
Blockly.Msg["PROCEDURES_DEFRETURN_HELPURL"] = "https://en.wikipedia.org/wiki/Subroutine";  // untranslated
Blockly.Msg["PROCEDURES_DEFRETURN_RETURN"] = "zréck";
Blockly.Msg["PROCEDURES_DEFRETURN_TOOLTIP"] = "Creates a function with an output.";  // untranslated
Blockly.Msg["PROCEDURES_DEF_DUPLICATE_WARNING"] = "Warning: This function has duplicate parameters.";  // untranslated
Blockly.Msg["PROCEDURES_HIGHLIGHT_DEF"] = "Highlight function definition";  // untranslated
Blockly.Msg["PROCEDURES_IFRETURN_HELPURL"] = "http://c2.com/cgi/wiki?GuardClause";  // untranslated
Blockly.Msg["PROCEDURES_IFRETURN_TOOLTIP"] = "If a value is true, then return a second value.";  // untranslated
Blockly.Msg["PROCEDURES_IFRETURN_WARNING"] = "Warning: This block may be used only within a function definition.";  // untranslated
Blockly.Msg["PROCEDURES_MUTATORARG_TITLE"] = "input name:";  // untranslated
Blockly.Msg["PROCEDURES_MUTATORARG_TOOLTIP"] = "Add an input to the function.";  // untranslated
Blockly.Msg["PROCEDURES_MUTATORCONTAINER_TITLE"] = "inputs";  // untranslated
Blockly.Msg["PROCEDURES_MUTATORCONTAINER_TOOLTIP"] = "Add, remove, or reorder inputs to this function.";  // untranslated
Blockly.Msg["REDO"] = "Widderhuelen";
Blockly.Msg["REMOVE_COMMENT"] = "Bemierkung ewechhuelen";
Blockly.Msg["RENAME_VARIABLE"] = "Variabel ëmbenennen...";
Blockly.Msg["RENAME_VARIABLE_TITLE"] = "All '%1' Variabelen ëmbenennen op:";
Blockly.Msg["TEXT_APPEND_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-modification";  // untranslated
Blockly.Msg["TEXT_APPEND_TITLE"] = "to %1 append text %2";  // untranslated
Blockly.Msg["TEXT_APPEND_TOOLTIP"] = "Append some text to variable '%1'.";  // untranslated
Blockly.Msg["TEXT_CHANGECASE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#adjusting-text-case";  // untranslated
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_LOWERCASE"] = "to lower case";  // untranslated
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_TITLECASE"] = "to Title Case";  // untranslated
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_UPPERCASE"] = "to UPPER CASE";  // untranslated
Blockly.Msg["TEXT_CHANGECASE_TOOLTIP"] = "Return a copy of the text in a different case.";  // untranslated
Blockly.Msg["TEXT_CHARAT_FIRST"] = "get first letter";  // untranslated
Blockly.Msg["TEXT_CHARAT_FROM_END"] = "get letter # from end";  // untranslated
Blockly.Msg["TEXT_CHARAT_FROM_START"] = "get letter #";  // untranslated
Blockly.Msg["TEXT_CHARAT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#extracting-text";  // untranslated
Blockly.Msg["TEXT_CHARAT_LAST"] = "get last letter";  // untranslated
Blockly.Msg["TEXT_CHARAT_RANDOM"] = "get random letter";  // untranslated
Blockly.Msg["TEXT_CHARAT_TAIL"] = "";  // untranslated
Blockly.Msg["TEXT_CHARAT_TITLE"] = "am Text %1 %2";
Blockly.Msg["TEXT_CHARAT_TOOLTIP"] = "Returns the letter at the specified position.";  // untranslated
Blockly.Msg["TEXT_COUNT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#counting-substrings";  // untranslated
Blockly.Msg["TEXT_COUNT_MESSAGE0"] = "count %1 in %2";  // untranslated
Blockly.Msg["TEXT_COUNT_TOOLTIP"] = "Count how many times some text occurs within some other text.";  // untranslated
Blockly.Msg["TEXT_CREATE_JOIN_ITEM_TOOLTIP"] = "En Element bei den Text derbäisetzen.";
Blockly.Msg["TEXT_CREATE_JOIN_TITLE_JOIN"] = "join";  // untranslated
Blockly.Msg["TEXT_CREATE_JOIN_TOOLTIP"] = "Add, remove, or reorder sections to reconfigure this text block.";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_END_FROM_END"] = "to letter # from end";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_END_FROM_START"] = "bis bei de Buschtaf #";
Blockly.Msg["TEXT_GET_SUBSTRING_END_LAST"] = "bis bei de leschte Buschtaf";
Blockly.Msg["TEXT_GET_SUBSTRING_HELPURL"] = "https://github.com/google/blockly/wiki/Text#extracting-a-region-of-text";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_INPUT_IN_TEXT"] = "am Text";
Blockly.Msg["TEXT_GET_SUBSTRING_START_FIRST"] = "get substring from first letter";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_START_FROM_END"] = "get substring from letter # from end";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_START_FROM_START"] = "get substring from letter #";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_TAIL"] = "";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_TOOLTIP"] = "Returns a specified portion of the text.";  // untranslated
Blockly.Msg["TEXT_INDEXOF_HELPURL"] = "https://github.com/google/blockly/wiki/Text#finding-text";  // untranslated
Blockly.Msg["TEXT_INDEXOF_OPERATOR_FIRST"] = "find first occurrence of text";  // untranslated
Blockly.Msg["TEXT_INDEXOF_OPERATOR_LAST"] = "find last occurrence of text";  // untranslated
Blockly.Msg["TEXT_INDEXOF_TITLE"] = "am Text %1 %2 %3";
Blockly.Msg["TEXT_INDEXOF_TOOLTIP"] = "Returns the index of the first/last occurrence of the first text in the second text. Returns %1 if text is not found.";  // untranslated
Blockly.Msg["TEXT_ISEMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Text#checking-for-empty-text";  // untranslated
Blockly.Msg["TEXT_ISEMPTY_TITLE"] = "%1 ass eidel";
Blockly.Msg["TEXT_ISEMPTY_TOOLTIP"] = "Returns true if the provided text is empty.";  // untranslated
Blockly.Msg["TEXT_JOIN_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-creation";  // untranslated
Blockly.Msg["TEXT_JOIN_TITLE_CREATEWITH"] = "create text with";  // untranslated
Blockly.Msg["TEXT_JOIN_TOOLTIP"] = "Create a piece of text by joining together any number of items.";  // untranslated
Blockly.Msg["TEXT_LENGTH_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-modification";  // untranslated
Blockly.Msg["TEXT_LENGTH_TITLE"] = "Längt vu(n) %1";
Blockly.Msg["TEXT_LENGTH_TOOLTIP"] = "Returns the number of letters (including spaces) in the provided text.";  // untranslated
Blockly.Msg["TEXT_PRINT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#printing-text";  // untranslated
Blockly.Msg["TEXT_PRINT_TITLE"] = "%1 drécken";
Blockly.Msg["TEXT_PRINT_TOOLTIP"] = "Print the specified text, number or other value.";  // untranslated
Blockly.Msg["TEXT_PROMPT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#getting-input-from-the-user";  // untranslated
Blockly.Msg["TEXT_PROMPT_TOOLTIP_NUMBER"] = "Prompt for user for a number.";  // untranslated
Blockly.Msg["TEXT_PROMPT_TOOLTIP_TEXT"] = "Frot de Benotzer no engem Text.";
Blockly.Msg["TEXT_PROMPT_TYPE_NUMBER"] = "prompt for number with message";  // untranslated
Blockly.Msg["TEXT_PROMPT_TYPE_TEXT"] = "prompt for text with message";  // untranslated
Blockly.Msg["TEXT_REPLACE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#replacing-substrings";  // untranslated
Blockly.Msg["TEXT_REPLACE_MESSAGE0"] = "%1 duerch %2 a(n) %3 ersetzen";
Blockly.Msg["TEXT_REPLACE_TOOLTIP"] = "All Kéiers wou e bestëmmten Text do ass duerch en aneren Text ersetzen.";
Blockly.Msg["TEXT_REVERSE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#reversing-text";  // untranslated
Blockly.Msg["TEXT_REVERSE_MESSAGE0"] = "reverse %1";  // untranslated
Blockly.Msg["TEXT_REVERSE_TOOLTIP"] = "Dréint d'Reiefolleg vun den Zeechen am Text ëm.";
Blockly.Msg["TEXT_TEXT_HELPURL"] = "https://en.wikipedia.org/wiki/String_(computer_science)";  // untranslated
Blockly.Msg["TEXT_TEXT_TOOLTIP"] = "E Buschtaf, e Wuert oder eng Textzeil.";
Blockly.Msg["TEXT_TRIM_HELPURL"] = "https://github.com/google/blockly/wiki/Text#trimming-removing-spaces";  // untranslated
Blockly.Msg["TEXT_TRIM_OPERATOR_BOTH"] = "trim spaces from both sides of";  // untranslated
Blockly.Msg["TEXT_TRIM_OPERATOR_LEFT"] = "trim spaces from left side of";  // untranslated
Blockly.Msg["TEXT_TRIM_OPERATOR_RIGHT"] = "trim spaces from right side of";  // untranslated
Blockly.Msg["TEXT_TRIM_TOOLTIP"] = "Return a copy of the text with spaces removed from one or both ends.";  // untranslated
Blockly.Msg["TODAY"] = "Haut";
Blockly.Msg["UNDO"] = "Réckgängeg maachen";
Blockly.Msg["UNNAMED_KEY"] = "ouni Numm";
Blockly.Msg["VARIABLES_DEFAULT_NAME"] = "Element";
Blockly.Msg["VARIABLES_GET_CREATE_SET"] = "Create 'set %1'";  // untranslated
Blockly.Msg["VARIABLES_GET_HELPURL"] = "https://github.com/google/blockly/wiki/Variables#get";  // untranslated
Blockly.Msg["VARIABLES_GET_TOOLTIP"] = "Returns the value of this variable.";  // untranslated
Blockly.Msg["VARIABLES_SET"] = "set %1 to %2";  // untranslated
Blockly.Msg["VARIABLES_SET_CREATE_GET"] = "Create 'get %1'";  // untranslated
Blockly.Msg["VARIABLES_SET_HELPURL"] = "https://github.com/google/blockly/wiki/Variables#set";  // untranslated
Blockly.Msg["VARIABLES_SET_TOOLTIP"] = "Sets this variable to be equal to the input.";  // untranslated
Blockly.Msg["VARIABLE_ALREADY_EXISTS"] = "A variable named '%1' already exists.";  // untranslated
Blockly.Msg["VARIABLE_ALREADY_EXISTS_FOR_ANOTHER_TYPE"] = "A variable named '%1' already exists for another type: '%2'.";  // untranslated
Blockly.Msg["WORKSPACE_ARIA_LABEL"] = "Blockly Workspace";  // untranslated
Blockly.Msg["WORKSPACE_COMMENT_DEFAULT_TEXT"] = "Sot eppes...";
Blockly.Msg["CONTROLS_FOREACH_INPUT_DO"] = Blockly.Msg["CONTROLS_REPEAT_INPUT_DO"];
Blockly.Msg["CONTROLS_FOR_INPUT_DO"] = Blockly.Msg["CONTROLS_REPEAT_INPUT_DO"];
Blockly.Msg["CONTROLS_IF_ELSEIF_TITLE_ELSEIF"] = Blockly.Msg["CONTROLS_IF_MSG_ELSEIF"];
Blockly.Msg["CONTROLS_IF_ELSE_TITLE_ELSE"] = Blockly.Msg["CONTROLS_IF_MSG_ELSE"];
Blockly.Msg["CONTROLS_IF_IF_TITLE_IF"] = Blockly.Msg["CONTROLS_IF_MSG_IF"];
Blockly.Msg["CONTROLS_IF_MSG_THEN"] = Blockly.Msg["CONTROLS_REPEAT_INPUT_DO"];
Blockly.Msg["CONTROLS_WHILEUNTIL_INPUT_DO"] = Blockly.Msg["CONTROLS_REPEAT_INPUT_DO"];
Blockly.Msg["LISTS_CREATE_WITH_ITEM_TITLE"] = Blockly.Msg["VARIABLES_DEFAULT_NAME"];
Blockly.Msg["LISTS_GET_INDEX_HELPURL"] = Blockly.Msg["LISTS_INDEX_OF_HELPURL"];
Blockly.Msg["LISTS_GET_INDEX_INPUT_IN_LIST"] = Blockly.Msg["LISTS_INLIST"];
Blockly.Msg["LISTS_GET_SUBLIST_INPUT_IN_LIST"] = Blockly.Msg["LISTS_INLIST"];
Blockly.Msg["LISTS_INDEX_OF_INPUT_IN_LIST"] = Blockly.Msg["LISTS_INLIST"];
Blockly.Msg["LISTS_SET_INDEX_INPUT_IN_LIST"] = Blockly.Msg["LISTS_INLIST"];
Blockly.Msg["MATH_CHANGE_TITLE_ITEM"] = Blockly.Msg["VARIABLES_DEFAULT_NAME"];
Blockly.Msg["PROCEDURES_DEFRETURN_COMMENT"] = Blockly.Msg["PROCEDURES_DEFNORETURN_COMMENT"];
Blockly.Msg["PROCEDURES_DEFRETURN_DO"] = Blockly.Msg["PROCEDURES_DEFNORETURN_DO"];
Blockly.Msg["PROCEDURES_DEFRETURN_PROCEDURE"] = Blockly.Msg["PROCEDURES_DEFNORETURN_PROCEDURE"];
Blockly.Msg["PROCEDURES_DEFRETURN_TITLE"] = Blockly.Msg["PROCEDURES_DEFNORETURN_TITLE"];
Blockly.Msg["TEXT_APPEND_VARIABLE"] = Blockly.Msg["VARIABLES_DEFAULT_NAME"];
Blockly.Msg["TEXT_CREATE_JOIN_ITEM_TITLE_ITEM"] = Blockly.Msg["VARIABLES_DEFAULT_NAME"];

Blockly.Msg["MATH_HUE"] = "230";
Blockly.Msg["LOOPS_HUE"] = "120";
Blockly.Msg["LISTS_HUE"] = "260";
Blockly.Msg["LOGIC_HUE"] = "210";
Blockly.Msg["VARIABLES_HUE"] = "330";
Blockly.Msg["TEXTS_HUE"] = "160";
Blockly.Msg["PROCEDURES_HUE"] = "290";
Blockly.Msg["COLOUR_HUE"] = "20";
Blockly.Msg["VARIABLES_DYNAMIC_HUE"] = "310";
return Blockly.Msg;
}));
