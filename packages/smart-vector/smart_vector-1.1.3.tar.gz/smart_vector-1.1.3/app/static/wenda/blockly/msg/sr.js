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

Blockly.Msg["ADD_COMMENT"] = "Додај коментар";
Blockly.Msg["CANNOT_DELETE_VARIABLE_PROCEDURE"] = "Није могуће избрисати променљиву „%1” јер је део дефиниције функције „%2”";
Blockly.Msg["CHANGE_VALUE_TITLE"] = "Промена вредности:";
Blockly.Msg["CLEAN_UP"] = "Очисти блокове";
Blockly.Msg["COLLAPSED_WARNINGS_WARNING"] = "Срушени блокови садрже упозорења.";
Blockly.Msg["COLLAPSE_ALL"] = "Скупи блокове";
Blockly.Msg["COLLAPSE_BLOCK"] = "Скупи блок";
Blockly.Msg["COLOUR_BLEND_COLOUR1"] = "боја 1";
Blockly.Msg["COLOUR_BLEND_COLOUR2"] = "боја 2";
Blockly.Msg["COLOUR_BLEND_HELPURL"] = "https://meyerweb.com/eric/tools/color-blend/#:::rgbp";  // untranslated
Blockly.Msg["COLOUR_BLEND_RATIO"] = "однос";
Blockly.Msg["COLOUR_BLEND_TITLE"] = "помешај";
Blockly.Msg["COLOUR_BLEND_TOOLTIP"] = "Меша две боје заједно са датим односом (0.0 - 1.0).";
Blockly.Msg["COLOUR_PICKER_HELPURL"] = "https://sr.wikipedia.org/wiki/Боја";
Blockly.Msg["COLOUR_PICKER_TOOLTIP"] = "Одаберите боју са палете.";
Blockly.Msg["COLOUR_RANDOM_HELPURL"] = "http://randomcolour.com";  // untranslated
Blockly.Msg["COLOUR_RANDOM_TITLE"] = "случајна боја";
Blockly.Msg["COLOUR_RANDOM_TOOLTIP"] = "Одаберите боју насумично.";
Blockly.Msg["COLOUR_RGB_BLUE"] = "плава";
Blockly.Msg["COLOUR_RGB_GREEN"] = "зелена";
Blockly.Msg["COLOUR_RGB_HELPURL"] = "https://www.december.com/html/spec/colorpercompact.html";  // untranslated
Blockly.Msg["COLOUR_RGB_RED"] = "црвена";
Blockly.Msg["COLOUR_RGB_TITLE"] = "боја са";
Blockly.Msg["COLOUR_RGB_TOOLTIP"] = "Направите боју са одређеном количином црвене, зелене и плаве. Све вредности морају бити између 0 и 100.";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#loop-termination-blocks";  // untranslated
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_OPERATOR_BREAK"] = "изађи из петље";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_OPERATOR_CONTINUE"] = "настави са следећом итерацијом петље";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_TOOLTIP_BREAK"] = "Напусти садржај петље.";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_TOOLTIP_CONTINUE"] = "Прескочи остатак ове петље, и настави са следећом итерацијом(понављанјем).";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_WARNING"] = "Упозорење: Овај блок може да се употреби само унутар петље.";
Blockly.Msg["CONTROLS_FOREACH_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#for-each";  // untranslated
Blockly.Msg["CONTROLS_FOREACH_TITLE"] = "за сваку ставку %1 на списку %2";
Blockly.Msg["CONTROLS_FOREACH_TOOLTIP"] = "За сваку ставку унутар листе, подеси промењиву '%1' по ставци, и онда начини неке изјаве-наредбе.";
Blockly.Msg["CONTROLS_FOR_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#count-with";  // untranslated
Blockly.Msg["CONTROLS_FOR_TITLE"] = "преброј са %1 од %2 до %3 од %4";
Blockly.Msg["CONTROLS_FOR_TOOLTIP"] = "Имај промењиву \"%1\" узми вредности од почетног броја до задњег броја, бројећи по одређеном интервалу, и изврши одређене блокове.";
Blockly.Msg["CONTROLS_IF_ELSEIF_TOOLTIP"] = "Додајте услов блоку „ако“.";
Blockly.Msg["CONTROLS_IF_ELSE_TOOLTIP"] = "Додај коначни, catch-all  (ухвати све) услове иф блока.";
Blockly.Msg["CONTROLS_IF_HELPURL"] = "https://github.com/google/blockly/wiki/IfElse";  // untranslated
Blockly.Msg["CONTROLS_IF_IF_TOOLTIP"] = "Додај, уклони, или преуреди делове како бих реконфигурисали овај иф блок.";
Blockly.Msg["CONTROLS_IF_MSG_ELSE"] = "иначе";
Blockly.Msg["CONTROLS_IF_MSG_ELSEIF"] = "иначе-ако";
Blockly.Msg["CONTROLS_IF_MSG_IF"] = "ако";
Blockly.Msg["CONTROLS_IF_TOOLTIP_1"] = "ако је вредност тачна, онда изврши неке наредбе-изјаве.";
Blockly.Msg["CONTROLS_IF_TOOLTIP_2"] = "ако је вредност тачна, онда изврши први блок наредби, У супротном, изврши други блок наредби.";
Blockly.Msg["CONTROLS_IF_TOOLTIP_3"] = "Ако је прва вредност тачна, онда изврши први блок наредби, у супротном, ако је друга вредност тачна , изврши други блок наредби.";
Blockly.Msg["CONTROLS_IF_TOOLTIP_4"] = "Ако је прва вредност тачна, онда изврши први блок наредби, у супротном, ако је друга вредност тачна , изврши други блок наредби. Ако ни једна од вредности није тачна, изврши последнји блок наредби.";
Blockly.Msg["CONTROLS_REPEAT_HELPURL"] = "https://sr.wikipedia.org/wiki/For_петља";
Blockly.Msg["CONTROLS_REPEAT_INPUT_DO"] = "изврши";
Blockly.Msg["CONTROLS_REPEAT_TITLE"] = "понови %1 пута";
Blockly.Msg["CONTROLS_REPEAT_TOOLTIP"] = "Изврши неке наредбе неколико пута.";
Blockly.Msg["CONTROLS_WHILEUNTIL_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#repeat";  // untranslated
Blockly.Msg["CONTROLS_WHILEUNTIL_OPERATOR_UNTIL"] = "понављати до";
Blockly.Msg["CONTROLS_WHILEUNTIL_OPERATOR_WHILE"] = "понављати док";
Blockly.Msg["CONTROLS_WHILEUNTIL_TOOLTIP_UNTIL"] = "Док је вредност нетачна, извршава неке наредбе.";
Blockly.Msg["CONTROLS_WHILEUNTIL_TOOLTIP_WHILE"] = "Док је вредност тачна, извршава неке наредбе.";
Blockly.Msg["DELETE_ALL_BLOCKS"] = "Избрисати свих %1 блокова?";
Blockly.Msg["DELETE_BLOCK"] = "Избриши блок";
Blockly.Msg["DELETE_VARIABLE"] = "Избриши променљиву ’%1’";
Blockly.Msg["DELETE_VARIABLE_CONFIRMATION"] = "Избрисати %1 употребу променљиве „%2”?";
Blockly.Msg["DELETE_X_BLOCKS"] = "Избриши %1 блокова";
Blockly.Msg["DIALOG_CANCEL"] = "Откажи";
Blockly.Msg["DIALOG_OK"] = "У реду";
Blockly.Msg["DISABLE_BLOCK"] = "Онемогући блок";
Blockly.Msg["DUPLICATE_BLOCK"] = "Дуплирај";
Blockly.Msg["DUPLICATE_COMMENT"] = "Дуплирај коментар";
Blockly.Msg["ENABLE_BLOCK"] = "Омогући блок";
Blockly.Msg["EXPAND_ALL"] = "Прошири блокове";
Blockly.Msg["EXPAND_BLOCK"] = "Прошири блок";
Blockly.Msg["EXTERNAL_INPUTS"] = "Спољашњи улази";
Blockly.Msg["HELP"] = "Помоћ";
Blockly.Msg["INLINE_INPUTS"] = "Редни улази";
Blockly.Msg["LISTS_CREATE_EMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-empty-list";  // untranslated
Blockly.Msg["LISTS_CREATE_EMPTY_TITLE"] = "направи празан списак";
Blockly.Msg["LISTS_CREATE_EMPTY_TOOLTIP"] = "Враћа списак, дужине 0, без података";
Blockly.Msg["LISTS_CREATE_WITH_CONTAINER_TITLE_ADD"] = "списак";
Blockly.Msg["LISTS_CREATE_WITH_CONTAINER_TOOLTIP"] = "Додајте, избришите, или преуредите делове како би се реорганизовали овај блок листе.";
Blockly.Msg["LISTS_CREATE_WITH_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-list-with";  // untranslated
Blockly.Msg["LISTS_CREATE_WITH_INPUT_WITH"] = "направи списак са";
Blockly.Msg["LISTS_CREATE_WITH_ITEM_TOOLTIP"] = "Додајте ставку на списак.";
Blockly.Msg["LISTS_CREATE_WITH_TOOLTIP"] = "Направите списак са било којим бројем ставки.";
Blockly.Msg["LISTS_GET_INDEX_FIRST"] = "прва";
Blockly.Msg["LISTS_GET_INDEX_FROM_END"] = "# са краја";
Blockly.Msg["LISTS_GET_INDEX_FROM_START"] = "#";
Blockly.Msg["LISTS_GET_INDEX_GET"] = "преузми";
Blockly.Msg["LISTS_GET_INDEX_GET_REMOVE"] = "преузми и уклони";
Blockly.Msg["LISTS_GET_INDEX_LAST"] = "последња";
Blockly.Msg["LISTS_GET_INDEX_RANDOM"] = "случајна";
Blockly.Msg["LISTS_GET_INDEX_REMOVE"] = "уклони";
Blockly.Msg["LISTS_GET_INDEX_TAIL"] = "";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_FIRST"] = "Враћа прву ставку на списку.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_FROM"] = "Враћа ставку на одређену позицију на списку.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_LAST"] = "Враћа последњу ставку са списка.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_RANDOM"] = "Враћа случајну ставку са списка.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_FIRST"] = "Уклања и враћа прву ставку са списка.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_FROM"] = "Уклања и враћа ставку са одређеног положаја са списка.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_LAST"] = "Уклања и враћа последњу ставку са списка.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_RANDOM"] = "Уклања и враћа случајну ставку са списка.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_FIRST"] = "Уклања прву ставку са списка.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_FROM"] = "Уклања ставку са одређеног положаја са списка.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_LAST"] = "Уклања последњу ставку са списка.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_RANDOM"] = "Уклања случајну ставку са списка.";
Blockly.Msg["LISTS_GET_SUBLIST_END_FROM_END"] = "до # од краја";
Blockly.Msg["LISTS_GET_SUBLIST_END_FROM_START"] = "до #";
Blockly.Msg["LISTS_GET_SUBLIST_END_LAST"] = "до последње";
Blockly.Msg["LISTS_GET_SUBLIST_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#getting-a-sublist";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_START_FIRST"] = "преузми подсписак од прве";
Blockly.Msg["LISTS_GET_SUBLIST_START_FROM_END"] = "преузми подсписак из # са краја";
Blockly.Msg["LISTS_GET_SUBLIST_START_FROM_START"] = "преузми подсписак од #";
Blockly.Msg["LISTS_GET_SUBLIST_TAIL"] = "";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_TOOLTIP"] = "Прави копију одређеног дела списка.";
Blockly.Msg["LISTS_INDEX_FROM_END_TOOLTIP"] = "%1 је последња ставка.";
Blockly.Msg["LISTS_INDEX_FROM_START_TOOLTIP"] = "%1 је прва ставка.";
Blockly.Msg["LISTS_INDEX_OF_FIRST"] = "пронађи прво појављивање ставке";
Blockly.Msg["LISTS_INDEX_OF_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#getting-items-from-a-list";  // untranslated
Blockly.Msg["LISTS_INDEX_OF_LAST"] = "пронађи последње појављивање ставке";
Blockly.Msg["LISTS_INDEX_OF_TOOLTIP"] = "Враћа индекс прве/последње појаве ставке на списку. Враћа %1 ако ставка није пронађена.";
Blockly.Msg["LISTS_INLIST"] = "на списку";
Blockly.Msg["LISTS_ISEMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#is-empty";  // untranslated
Blockly.Msg["LISTS_ISEMPTY_TITLE"] = "%1 је празан";
Blockly.Msg["LISTS_ISEMPTY_TOOLTIP"] = "Враћа вредност „тачно” ако је списак празан.";
Blockly.Msg["LISTS_LENGTH_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#length-of";  // untranslated
Blockly.Msg["LISTS_LENGTH_TITLE"] = "дужина списка %1";
Blockly.Msg["LISTS_LENGTH_TOOLTIP"] = "Враћа дужину списка.";
Blockly.Msg["LISTS_REPEAT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-list-with";  // untranslated
Blockly.Msg["LISTS_REPEAT_TITLE"] = "Направити списак са ставком %1 која се понавља %2 пута";
Blockly.Msg["LISTS_REPEAT_TOOLTIP"] = "Прави листу која се састоји од задане вредности коју понавлјамо одређени број шута.";
Blockly.Msg["LISTS_REVERSE_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#reversing-a-list";  // untranslated
Blockly.Msg["LISTS_REVERSE_MESSAGE0"] = "обрнуто %1";
Blockly.Msg["LISTS_REVERSE_TOOLTIP"] = "Обрни копију списка.";
Blockly.Msg["LISTS_SET_INDEX_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#in-list--set";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_INPUT_TO"] = "као";
Blockly.Msg["LISTS_SET_INDEX_INSERT"] = "убаци на";
Blockly.Msg["LISTS_SET_INDEX_SET"] = "постави";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_FIRST"] = "Убацује ставку на почетак списка.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_FROM"] = "Убацује ставку на одређени положај на списку.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_LAST"] = "Додајте ставку на крај списка.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_RANDOM"] = "Убацује ставку на случајно место на списку.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_FIRST"] = "Поставља прву ставку на списку.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_FROM"] = "Поставља ставку на одређени положај на списку.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_LAST"] = "Поставља последњу ставку на списку.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_RANDOM"] = "Поставља случајну ставку на списку.";
Blockly.Msg["LISTS_SORT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#sorting-a-list";  // untranslated
Blockly.Msg["LISTS_SORT_ORDER_ASCENDING"] = "растуће";
Blockly.Msg["LISTS_SORT_ORDER_DESCENDING"] = "опадајуће";
Blockly.Msg["LISTS_SORT_TITLE"] = "сортирај %1 %2 %3";
Blockly.Msg["LISTS_SORT_TOOLTIP"] = "Сортирајте копију списка.";
Blockly.Msg["LISTS_SORT_TYPE_IGNORECASE"] = "азбучно, игнориши мала и велика слова";
Blockly.Msg["LISTS_SORT_TYPE_NUMERIC"] = "као бројеве";
Blockly.Msg["LISTS_SORT_TYPE_TEXT"] = "азбучно";
Blockly.Msg["LISTS_SPLIT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#splitting-strings-and-joining-lists";  // untranslated
Blockly.Msg["LISTS_SPLIT_LIST_FROM_TEXT"] = "направите листу са текста";
Blockly.Msg["LISTS_SPLIT_TEXT_FROM_LIST"] = "направи текст из списка";
Blockly.Msg["LISTS_SPLIT_TOOLTIP_JOIN"] = "Спаја списак текстова у један текст, раздвојених граничником.";
Blockly.Msg["LISTS_SPLIT_TOOLTIP_SPLIT"] = "Раздваја текст у списак текстова, преламањем на сваком граничнику.";
Blockly.Msg["LISTS_SPLIT_WITH_DELIMITER"] = "са граничником";
Blockly.Msg["LOGIC_BOOLEAN_FALSE"] = "нетачно";
Blockly.Msg["LOGIC_BOOLEAN_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#values";  // untranslated
Blockly.Msg["LOGIC_BOOLEAN_TOOLTIP"] = "Враћа или „тачно“ или „нетачно“.";
Blockly.Msg["LOGIC_BOOLEAN_TRUE"] = "тачно";
Blockly.Msg["LOGIC_COMPARE_HELPURL"] = "https://sr.wikipedia.org/wiki/Неједнакост";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_EQ"] = "Враћа вредност „тачно“ ако су оба улаза једнака.";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_GT"] = "Враћа вредност „тачно“ ако је први унос већи од другог.";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_GTE"] = "Враћа вредност „тачно“ ако је први унос већи или једнак другом.";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_LT"] = "Враћа вредност „тачно“ ако је први унос мањи од другог.";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_LTE"] = "Враћа вредност „тачно“ ако је први унос мањи или једнак другом.";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_NEQ"] = "Враћа вредност „тачно“ ако су оба уноса неједнака.";
Blockly.Msg["LOGIC_NEGATE_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#not";  // untranslated
Blockly.Msg["LOGIC_NEGATE_TITLE"] = "није %1";
Blockly.Msg["LOGIC_NEGATE_TOOLTIP"] = "Враћа вредност „тачно“ ако је унос нетачан. Враћа вредност „нетачно“ ако је унос тачан.";
Blockly.Msg["LOGIC_NULL"] = "без вредности";
Blockly.Msg["LOGIC_NULL_HELPURL"] = "https://en.wikipedia.org/wiki/Nullable_type";  // untranslated
Blockly.Msg["LOGIC_NULL_TOOLTIP"] = "Враћа „без вредности“.";
Blockly.Msg["LOGIC_OPERATION_AND"] = "и";
Blockly.Msg["LOGIC_OPERATION_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#logical-operations";  // untranslated
Blockly.Msg["LOGIC_OPERATION_OR"] = "или";
Blockly.Msg["LOGIC_OPERATION_TOOLTIP_AND"] = "Враћа вредност „тачно“ ако су оба уноса тачна.";
Blockly.Msg["LOGIC_OPERATION_TOOLTIP_OR"] = "Враћа вредност „тачно“ ако је бар један од уноса тачан.";
Blockly.Msg["LOGIC_TERNARY_CONDITION"] = "проба";
Blockly.Msg["LOGIC_TERNARY_HELPURL"] = "https://en.wikipedia.org/wiki/%3F:";  // untranslated
Blockly.Msg["LOGIC_TERNARY_IF_FALSE"] = "ако је нетачно";
Blockly.Msg["LOGIC_TERNARY_IF_TRUE"] = "ако је тачно";
Blockly.Msg["LOGIC_TERNARY_TOOLTIP"] = "Проверите услов у „проба”. Ако је услов тачан, тада враћа „ако је тачно” вредност; у другом случају враћа „ако је нетачно” вредност.";
Blockly.Msg["MATH_ADDITION_SYMBOL"] = "+";  // untranslated
Blockly.Msg["MATH_ARITHMETIC_HELPURL"] = "https://sr.wikipedia.org/wiki/Аритметика";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_ADD"] = "Враћа збир два броја.";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_DIVIDE"] = "Враћа количник два броја.";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_MINUS"] = "Враћа разлику два броја.";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_MULTIPLY"] = "Враћа производ два броја.";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_POWER"] = "Враћа први број степенован другим.";
Blockly.Msg["MATH_ATAN2_HELPURL"] = "https://en.wikipedia.org/wiki/Atan2";  // untranslated
Blockly.Msg["MATH_ATAN2_TITLE"] = "атан2 од X:%1 Y:%2";
Blockly.Msg["MATH_ATAN2_TOOLTIP"] = "Врати арктангенту тачке (X, Y) у степенима од -180 до 180.";
Blockly.Msg["MATH_CHANGE_HELPURL"] = "https://en.wikipedia.org/wiki/Programming_idiom#Incrementing_a_counter";  // untranslated
Blockly.Msg["MATH_CHANGE_TITLE"] = "промени %1 за %2";
Blockly.Msg["MATH_CHANGE_TOOLTIP"] = "Додаје број променљивој „%1”.";
Blockly.Msg["MATH_CONSTANT_HELPURL"] = "https://sr.wikipedia.org/wiki/Математичка_константа";
Blockly.Msg["MATH_CONSTANT_TOOLTIP"] = "Враћа једну од заједничких константи: π (3.141…), e (2.718…), φ (1.618…), sqrt(2) (1.414…), sqrt(½) (0.707…), или ∞ (бесконачно).";
Blockly.Msg["MATH_CONSTRAIN_HELPURL"] = "https://en.wikipedia.org/wiki/Clamping_(graphics)";  // untranslated
Blockly.Msg["MATH_CONSTRAIN_TITLE"] = "ограничи %1 ниско %2 високо %3";
Blockly.Msg["MATH_CONSTRAIN_TOOLTIP"] = "Ограничава број на доње и горње границе (укључиво).";
Blockly.Msg["MATH_DIVISION_SYMBOL"] = "÷";  // untranslated
Blockly.Msg["MATH_IS_DIVISIBLE_BY"] = "је дељив са";
Blockly.Msg["MATH_IS_EVEN"] = "је паран";
Blockly.Msg["MATH_IS_NEGATIVE"] = "је негативан";
Blockly.Msg["MATH_IS_ODD"] = "је непаран";
Blockly.Msg["MATH_IS_POSITIVE"] = "је позитиван";
Blockly.Msg["MATH_IS_PRIME"] = "је прост";
Blockly.Msg["MATH_IS_TOOLTIP"] = "Проверава да ли је број паран, непаран, прост, цео, позитиван, негативан, или дељив са одређеним бројем. Враћа „тачно” или „нетачно”.";
Blockly.Msg["MATH_IS_WHOLE"] = "је цео";
Blockly.Msg["MATH_MODULO_HELPURL"] = "https://sr.wikipedia.org/wiki/Конгруенција";
Blockly.Msg["MATH_MODULO_TITLE"] = "подсетник од %1 ÷ %2";
Blockly.Msg["MATH_MODULO_TOOLTIP"] = "Враћа подсетник од дељења два броја.";
Blockly.Msg["MATH_MULTIPLICATION_SYMBOL"] = "×";  // untranslated
Blockly.Msg["MATH_NUMBER_HELPURL"] = "https://sr.wikipedia.org/wiki/Број";
Blockly.Msg["MATH_NUMBER_TOOLTIP"] = "Број.";
Blockly.Msg["MATH_ONLIST_HELPURL"] = "";  // untranslated
Blockly.Msg["MATH_ONLIST_OPERATOR_AVERAGE"] = "просек списка";
Blockly.Msg["MATH_ONLIST_OPERATOR_MAX"] = "макс. списка";
Blockly.Msg["MATH_ONLIST_OPERATOR_MEDIAN"] = "медијана списка";
Blockly.Msg["MATH_ONLIST_OPERATOR_MIN"] = "мин. списка";
Blockly.Msg["MATH_ONLIST_OPERATOR_MODE"] = "модус списка";
Blockly.Msg["MATH_ONLIST_OPERATOR_RANDOM"] = "случајна ставка списка";
Blockly.Msg["MATH_ONLIST_OPERATOR_STD_DEV"] = "стандардна девијација списка";
Blockly.Msg["MATH_ONLIST_OPERATOR_SUM"] = "збир списка";
Blockly.Msg["MATH_ONLIST_TOOLTIP_AVERAGE"] = "Враћа просек (аритметичку средину) бројева са списка.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MAX"] = "Враћа највећи број са списка.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MEDIAN"] = "Враћа медијану са списка.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MIN"] = "Враћа најмањи број са списка.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MODE"] = "Враћа списак најчешћих ставки на списку.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_RANDOM"] = "Враћа случајни елемент са списка.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_STD_DEV"] = "Враћа стандардну девијацију списка.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_SUM"] = "Враћа збир свих бројева са списка.";
Blockly.Msg["MATH_POWER_SYMBOL"] = "^";  // untranslated
Blockly.Msg["MATH_RANDOM_FLOAT_HELPURL"] = "https://sr.wikipedia.org/wiki/Генератор_случајних_бројева";
Blockly.Msg["MATH_RANDOM_FLOAT_TITLE_RANDOM"] = "случајни разломак";
Blockly.Msg["MATH_RANDOM_FLOAT_TOOLTIP"] = "Враћа случајни разломак између 0.0 (укључиво) и 1.0 (искључиво).";
Blockly.Msg["MATH_RANDOM_INT_HELPURL"] = "https://sr.wikipedia.org/wiki/Генератор_случајних_бројева";
Blockly.Msg["MATH_RANDOM_INT_TITLE"] = "сличајно одабрани цијели број од %1 до %2";
Blockly.Msg["MATH_RANDOM_INT_TOOLTIP"] = "Враћа случајно одабрани цели број између две одређене границе, уклјучиво.";
Blockly.Msg["MATH_ROUND_HELPURL"] = "https://sr.wikipedia.org/wiki/Заокруживање";
Blockly.Msg["MATH_ROUND_OPERATOR_ROUND"] = "заокружи";
Blockly.Msg["MATH_ROUND_OPERATOR_ROUNDDOWN"] = "заокружи наниже";
Blockly.Msg["MATH_ROUND_OPERATOR_ROUNDUP"] = "заокружи навише";
Blockly.Msg["MATH_ROUND_TOOLTIP"] = "Заокружује број на већу или мању вредност.";
Blockly.Msg["MATH_SINGLE_HELPURL"] = "https://sr.wikipedia.org/wiki/Квадратни_корен";
Blockly.Msg["MATH_SINGLE_OP_ABSOLUTE"] = "апсолутно";
Blockly.Msg["MATH_SINGLE_OP_ROOT"] = "квадратни корен";
Blockly.Msg["MATH_SINGLE_TOOLTIP_ABS"] = "Враћа апсолутну вредност броја.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_EXP"] = "Враћа е-број на степен броја.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_LN"] = "Враћа природни логаритам броја.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_LOG10"] = "Враћа логаритам броја са основом 10.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_NEG"] = "Враћа негацију броја.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_POW10"] = "Враћа 10-ти степен броја.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_ROOT"] = "Враћа квадратни корен броја.";
Blockly.Msg["MATH_SUBTRACTION_SYMBOL"] = "-";  // untranslated
Blockly.Msg["MATH_TRIG_ACOS"] = "арц цос";
Blockly.Msg["MATH_TRIG_ASIN"] = "арц син";
Blockly.Msg["MATH_TRIG_ATAN"] = "арц тан";
Blockly.Msg["MATH_TRIG_COS"] = "цос";
Blockly.Msg["MATH_TRIG_HELPURL"] = "https://sr.wikipedia.org/wiki/Тригонометријске_функције";
Blockly.Msg["MATH_TRIG_SIN"] = "син";
Blockly.Msg["MATH_TRIG_TAN"] = "тан";
Blockly.Msg["MATH_TRIG_TOOLTIP_ACOS"] = "Враћа аркус косинус броја.";
Blockly.Msg["MATH_TRIG_TOOLTIP_ASIN"] = "Враћа аркус синус броја.";
Blockly.Msg["MATH_TRIG_TOOLTIP_ATAN"] = "Враћа аркус тангенс броја.";
Blockly.Msg["MATH_TRIG_TOOLTIP_COS"] = "Враћа косинус степена (не радијан).";
Blockly.Msg["MATH_TRIG_TOOLTIP_SIN"] = "Враћа синус степена (не радијан).";
Blockly.Msg["MATH_TRIG_TOOLTIP_TAN"] = "Враћа тангенс степена (не радијан).";
Blockly.Msg["NEW_COLOUR_VARIABLE"] = "Направи променљиву боје...";
Blockly.Msg["NEW_NUMBER_VARIABLE"] = "Направи променљиву броја...";
Blockly.Msg["NEW_STRING_VARIABLE"] = "Направи променљиву ниске...";
Blockly.Msg["NEW_VARIABLE"] = "Направи променљиву…";
Blockly.Msg["NEW_VARIABLE_TITLE"] = "Име нове променљиве:";
Blockly.Msg["NEW_VARIABLE_TYPE_TITLE"] = "Нова врста променљиве:";
Blockly.Msg["ORDINAL_NUMBER_SUFFIX"] = "";  // untranslated
Blockly.Msg["PROCEDURES_ALLOW_STATEMENTS"] = "дозволи изјаве";
Blockly.Msg["PROCEDURES_BEFORE_PARAMS"] = "са:";
Blockly.Msg["PROCEDURES_CALLNORETURN_HELPURL"] = "https://sr.wikipedia.org/wiki/Потпрограм";
Blockly.Msg["PROCEDURES_CALLNORETURN_TOOLTIP"] = "Покреће кориснички дефинисану функцију „%1”.";
Blockly.Msg["PROCEDURES_CALLRETURN_HELPURL"] = "https://sr.wikipedia.org/wiki/Потпрограм";
Blockly.Msg["PROCEDURES_CALLRETURN_TOOLTIP"] = "Покреће кориснички дефинисану функцију „%1” и користи њен излаз.";
Blockly.Msg["PROCEDURES_CALL_BEFORE_PARAMS"] = "са:";
Blockly.Msg["PROCEDURES_CREATE_DO"] = "Направи „%1”";
Blockly.Msg["PROCEDURES_DEFNORETURN_COMMENT"] = "Опишите ову функцију…";
Blockly.Msg["PROCEDURES_DEFNORETURN_DO"] = "";  // untranslated
Blockly.Msg["PROCEDURES_DEFNORETURN_HELPURL"] = "https://en.wikipedia.org/wiki/Subroutine";  // untranslated
Blockly.Msg["PROCEDURES_DEFNORETURN_PROCEDURE"] = "урадите нешто";
Blockly.Msg["PROCEDURES_DEFNORETURN_TITLE"] = "до";
Blockly.Msg["PROCEDURES_DEFNORETURN_TOOLTIP"] = "Прави функцију без излаза.";
Blockly.Msg["PROCEDURES_DEFRETURN_HELPURL"] = "https://en.wikipedia.org/wiki/Subroutine";  // untranslated
Blockly.Msg["PROCEDURES_DEFRETURN_RETURN"] = "врати";
Blockly.Msg["PROCEDURES_DEFRETURN_TOOLTIP"] = "Прави функцију са излазом.";
Blockly.Msg["PROCEDURES_DEF_DUPLICATE_WARNING"] = "Упозорење: Ова функција има дуплиране параметре.";
Blockly.Msg["PROCEDURES_HIGHLIGHT_DEF"] = "Истакни дефиницију функције";
Blockly.Msg["PROCEDURES_IFRETURN_HELPURL"] = "http://c2.com/cgi/wiki?GuardClause";  // untranslated
Blockly.Msg["PROCEDURES_IFRETURN_TOOLTIP"] = "Ако је прва вредност тачна, враћа другу вредност.";
Blockly.Msg["PROCEDURES_IFRETURN_WARNING"] = "Упозорење: Овај блок се може користити једино унутар дефиниције функције.";
Blockly.Msg["PROCEDURES_MUTATORARG_TITLE"] = "име параметра:";
Blockly.Msg["PROCEDURES_MUTATORARG_TOOLTIP"] = "Додајте улазни параметар финкцији.";
Blockly.Msg["PROCEDURES_MUTATORCONTAINER_TITLE"] = "улази";
Blockly.Msg["PROCEDURES_MUTATORCONTAINER_TOOLTIP"] = "Додајте, уклоните или преуредите уносе за ову функцију.";
Blockly.Msg["REDO"] = "Понови";
Blockly.Msg["REMOVE_COMMENT"] = "Уклони коментар";
Blockly.Msg["RENAME_VARIABLE"] = "Преименуј променљиву…";
Blockly.Msg["RENAME_VARIABLE_TITLE"] = "Преименуј све ’%1’ променљиве у:";
Blockly.Msg["TEXT_APPEND_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-modification";  // untranslated
Blockly.Msg["TEXT_APPEND_TITLE"] = "на %1 додај текст %2";
Blockly.Msg["TEXT_APPEND_TOOLTIP"] = "Додаје текст променљивој „%1”.";
Blockly.Msg["TEXT_CHANGECASE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#adjusting-text-case";  // untranslated
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_LOWERCASE"] = "малим словима";
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_TITLECASE"] = "свака реч великим словом";
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_UPPERCASE"] = "великим словима";
Blockly.Msg["TEXT_CHANGECASE_TOOLTIP"] = "Враћа примерак текста са другачијом величином слова.";
Blockly.Msg["TEXT_CHARAT_FIRST"] = "преузми прво слово";
Blockly.Msg["TEXT_CHARAT_FROM_END"] = "преузми слово # са краја";
Blockly.Msg["TEXT_CHARAT_FROM_START"] = "преузми слово #";
Blockly.Msg["TEXT_CHARAT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#extracting-text";  // untranslated
Blockly.Msg["TEXT_CHARAT_LAST"] = "преузми последње слово";
Blockly.Msg["TEXT_CHARAT_RANDOM"] = "преузми случајно слово";
Blockly.Msg["TEXT_CHARAT_TAIL"] = "";  // untranslated
Blockly.Msg["TEXT_CHARAT_TITLE"] = "у тексту %1 %2";
Blockly.Msg["TEXT_CHARAT_TOOLTIP"] = "Враћа слово на одређени положај.";
Blockly.Msg["TEXT_COUNT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#counting-substrings";  // untranslated
Blockly.Msg["TEXT_COUNT_MESSAGE0"] = "број %1 у %2";
Blockly.Msg["TEXT_COUNT_TOOLTIP"] = "Броји колико пута се неки текст појављује унутар неког другог текста.";
Blockly.Msg["TEXT_CREATE_JOIN_ITEM_TOOLTIP"] = "Додајте ставку у текст.";
Blockly.Msg["TEXT_CREATE_JOIN_TITLE_JOIN"] = "спој";
Blockly.Msg["TEXT_CREATE_JOIN_TOOLTIP"] = "Додај, уклони, или другачије поредај одјелке како би изнова поставили овај текст блок.";
Blockly.Msg["TEXT_GET_SUBSTRING_END_FROM_END"] = "слову # са краја";
Blockly.Msg["TEXT_GET_SUBSTRING_END_FROM_START"] = "слову #";
Blockly.Msg["TEXT_GET_SUBSTRING_END_LAST"] = "последњем слову";
Blockly.Msg["TEXT_GET_SUBSTRING_HELPURL"] = "https://github.com/google/blockly/wiki/Text#extracting-a-region-of-text";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_INPUT_IN_TEXT"] = "у тексту";
Blockly.Msg["TEXT_GET_SUBSTRING_START_FIRST"] = "преузми подниску из првог слова";
Blockly.Msg["TEXT_GET_SUBSTRING_START_FROM_END"] = "преузми подниску из слова # са краја";
Blockly.Msg["TEXT_GET_SUBSTRING_START_FROM_START"] = "преузми подниску из слова #";
Blockly.Msg["TEXT_GET_SUBSTRING_TAIL"] = "";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_TOOLTIP"] = "Враћа одређени део текста.";
Blockly.Msg["TEXT_INDEXOF_HELPURL"] = "https://github.com/google/blockly/wiki/Text#finding-text";  // untranslated
Blockly.Msg["TEXT_INDEXOF_OPERATOR_FIRST"] = "пронађи прво појављивање текста";
Blockly.Msg["TEXT_INDEXOF_OPERATOR_LAST"] = "пронађи последње појављивање текста";
Blockly.Msg["TEXT_INDEXOF_TITLE"] = "у тексту %1 %2 %3";
Blockly.Msg["TEXT_INDEXOF_TOOLTIP"] = "Враћа индекс првог/задњег појављивања првог текста у другом тексту. Враћа %1 ако текст није пронађен.";
Blockly.Msg["TEXT_ISEMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Text#checking-for-empty-text";  // untranslated
Blockly.Msg["TEXT_ISEMPTY_TITLE"] = "%1 је празан";
Blockly.Msg["TEXT_ISEMPTY_TOOLTIP"] = "Враћа „тачно” ако је достављени текст празан.";
Blockly.Msg["TEXT_JOIN_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-creation";  // untranslated
Blockly.Msg["TEXT_JOIN_TITLE_CREATEWITH"] = "напиши текст са";
Blockly.Msg["TEXT_JOIN_TOOLTIP"] = "Направити дио текста спајајући различите ставке.";
Blockly.Msg["TEXT_LENGTH_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-modification";  // untranslated
Blockly.Msg["TEXT_LENGTH_TITLE"] = "дужина текста %1";
Blockly.Msg["TEXT_LENGTH_TOOLTIP"] = "Враћа број слова (уклјучујући размаке) у датом тексту.";
Blockly.Msg["TEXT_PRINT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#printing-text";  // untranslated
Blockly.Msg["TEXT_PRINT_TITLE"] = "прикажи %1";
Blockly.Msg["TEXT_PRINT_TOOLTIP"] = "Прикажите одређени текст, број или другу вредност на екрану.";
Blockly.Msg["TEXT_PROMPT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#getting-input-from-the-user";  // untranslated
Blockly.Msg["TEXT_PROMPT_TOOLTIP_NUMBER"] = "Питајте корисника за број.";
Blockly.Msg["TEXT_PROMPT_TOOLTIP_TEXT"] = "Питајте корисника за унос текста.";
Blockly.Msg["TEXT_PROMPT_TYPE_NUMBER"] = "питај за број са поруком";
Blockly.Msg["TEXT_PROMPT_TYPE_TEXT"] = "питај за текст са поруком";
Blockly.Msg["TEXT_REPLACE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#replacing-substrings";  // untranslated
Blockly.Msg["TEXT_REPLACE_MESSAGE0"] = "замена %1 са %2 у %3";
Blockly.Msg["TEXT_REPLACE_TOOLTIP"] = "Замена свих појава неког текста унутар неког другог текста.";
Blockly.Msg["TEXT_REVERSE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#reversing-text";  // untranslated
Blockly.Msg["TEXT_REVERSE_MESSAGE0"] = "обрнуто %1";
Blockly.Msg["TEXT_REVERSE_TOOLTIP"] = "Обрће редослед карактера у тексту.";
Blockly.Msg["TEXT_TEXT_HELPURL"] = "https://sr.wikipedia.org/wiki/Ниска";
Blockly.Msg["TEXT_TEXT_TOOLTIP"] = "Слово, реч или ред текста.";
Blockly.Msg["TEXT_TRIM_HELPURL"] = "https://github.com/google/blockly/wiki/Text#trimming-removing-spaces";  // untranslated
Blockly.Msg["TEXT_TRIM_OPERATOR_BOTH"] = "трим празнине са обе стране";
Blockly.Msg["TEXT_TRIM_OPERATOR_LEFT"] = "скратити простор са леве стране";
Blockly.Msg["TEXT_TRIM_OPERATOR_RIGHT"] = "скратити простор са десне стране";
Blockly.Msg["TEXT_TRIM_TOOLTIP"] = "Враћа копију текста са уклонјеним простором са једног од два краја.";
Blockly.Msg["TODAY"] = "Данас";
Blockly.Msg["UNDO"] = "Опозови";
Blockly.Msg["UNNAMED_KEY"] = "неименовано";
Blockly.Msg["VARIABLES_DEFAULT_NAME"] = "ставка";
Blockly.Msg["VARIABLES_GET_CREATE_SET"] = "Направи блок за доделу вредности %1";
Blockly.Msg["VARIABLES_GET_HELPURL"] = "https://github.com/google/blockly/wiki/Variables#get";  // untranslated
Blockly.Msg["VARIABLES_GET_TOOLTIP"] = "Враћа вредност ове променљиве.";
Blockly.Msg["VARIABLES_SET"] = "постави %1 у %2";
Blockly.Msg["VARIABLES_SET_CREATE_GET"] = "Направи блок за преузимање вредности из „%1”";
Blockly.Msg["VARIABLES_SET_HELPURL"] = "https://github.com/google/blockly/wiki/Variables#set";  // untranslated
Blockly.Msg["VARIABLES_SET_TOOLTIP"] = "Поставља променљиву тако да буде једнака улазу.";
Blockly.Msg["VARIABLE_ALREADY_EXISTS"] = "Променљива под именом ’%1’ већ постоји.";
Blockly.Msg["VARIABLE_ALREADY_EXISTS_FOR_ANOTHER_TYPE"] = "Променљива под именом ’%1’ већ постоји за други тип: ’%2’.";
Blockly.Msg["WORKSPACE_ARIA_LABEL"] = "Блоклијев радни простор";
Blockly.Msg["WORKSPACE_COMMENT_DEFAULT_TEXT"] = "Кажите нешто…";
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
