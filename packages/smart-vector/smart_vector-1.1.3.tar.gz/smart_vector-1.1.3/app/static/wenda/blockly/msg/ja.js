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

Blockly.Msg["ADD_COMMENT"] = "コメントを追加";
Blockly.Msg["CANNOT_DELETE_VARIABLE_PROCEDURE"] = "変数 '%1' は関数 '%2' の定義の一部であるため、削除できません";
Blockly.Msg["CHANGE_VALUE_TITLE"] = "値を変える：";
Blockly.Msg["CLEAN_UP"] = "ブロックを整理する";
Blockly.Msg["COLLAPSED_WARNINGS_WARNING"] = "つぶしたブロックには警告が入っています。";
Blockly.Msg["COLLAPSE_ALL"] = "ブロックを折りたたむ";
Blockly.Msg["COLLAPSE_BLOCK"] = "ブロックを折りたたむ";
Blockly.Msg["COLOUR_BLEND_COLOUR1"] = "色 1";
Blockly.Msg["COLOUR_BLEND_COLOUR2"] = "色 2";
Blockly.Msg["COLOUR_BLEND_HELPURL"] = "https://meyerweb.com/eric/tools/color-blend/#:::rgbp";  // untranslated
Blockly.Msg["COLOUR_BLEND_RATIO"] = "比率";
Blockly.Msg["COLOUR_BLEND_TITLE"] = "ブレンド";
Blockly.Msg["COLOUR_BLEND_TOOLTIP"] = "2色を与えられた比率（0.0～1.0）で混ぜます。";
Blockly.Msg["COLOUR_PICKER_HELPURL"] = "https://ja.wikipedia.org/wiki/色";
Blockly.Msg["COLOUR_PICKER_TOOLTIP"] = "パレットから色を選んでください。";
Blockly.Msg["COLOUR_RANDOM_HELPURL"] = "http://randomcolour.com";  // untranslated
Blockly.Msg["COLOUR_RANDOM_TITLE"] = "ランダムな色";
Blockly.Msg["COLOUR_RANDOM_TOOLTIP"] = "ランダムに色を選ぶ。";
Blockly.Msg["COLOUR_RGB_BLUE"] = "青";
Blockly.Msg["COLOUR_RGB_GREEN"] = "緑";
Blockly.Msg["COLOUR_RGB_HELPURL"] = "https://www.december.com/html/spec/colorpercompact.html";  // untranslated
Blockly.Msg["COLOUR_RGB_RED"] = "赤";
Blockly.Msg["COLOUR_RGB_TITLE"] = "色:";
Blockly.Msg["COLOUR_RGB_TOOLTIP"] = "赤、緑、および青の指定された量で色を作成します。すべての値は 0 ～ 100 の間でなければなりません。";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#loop-termination-blocks";  // untranslated
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_OPERATOR_BREAK"] = "ループから抜け出す";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_OPERATOR_CONTINUE"] = "ループの次の反復処理を続行します";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_TOOLTIP_BREAK"] = "入っているループから抜け出します。";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_TOOLTIP_CONTINUE"] = "このループの残りの部分をスキップして、ループの繰り返しを続けます。";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_WARNING"] = "注意: このブロックは、ループ内でのみ使用できます。";
Blockly.Msg["CONTROLS_FOREACH_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#for-each";  // untranslated
Blockly.Msg["CONTROLS_FOREACH_TITLE"] = "リスト%2の各項目%1について";
Blockly.Msg["CONTROLS_FOREACH_TOOLTIP"] = "リストの各項目について、その項目を変数'%1'として、いくつかのステートメントを実行します。";
Blockly.Msg["CONTROLS_FOR_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#count-with";  // untranslated
Blockly.Msg["CONTROLS_FOR_TITLE"] = "%1 を %2 から %3 まで %4 ずつカウントする";
Blockly.Msg["CONTROLS_FOR_TOOLTIP"] = "変数 '%1' が開始番号から終了番号まで指定した間隔での値をとって、指定したブロックを実行する。";
Blockly.Msg["CONTROLS_IF_ELSEIF_TOOLTIP"] = "「もしも」のブロックに条件を追加します。";
Blockly.Msg["CONTROLS_IF_ELSE_TOOLTIP"] = "Ifブロックに、すべてをキャッチする条件を追加。";
Blockly.Msg["CONTROLS_IF_HELPURL"] = "https://github.com/google/blockly/wiki/IfElse";  // untranslated
Blockly.Msg["CONTROLS_IF_IF_TOOLTIP"] = "追加、削除、またはセクションを順序変更して、ブロックをこれを再構成します。";
Blockly.Msg["CONTROLS_IF_MSG_ELSE"] = "そうでなければ";
Blockly.Msg["CONTROLS_IF_MSG_ELSEIF"] = "そうでなくもし";
Blockly.Msg["CONTROLS_IF_MSG_IF"] = "もし";
Blockly.Msg["CONTROLS_IF_TOOLTIP_1"] = "値が true の場合、ステートメントを実行します。";
Blockly.Msg["CONTROLS_IF_TOOLTIP_2"] = "値が true の場合は、最初のステートメントのブロックを実行します。それ以外の場合は、2番目のステートメントのブロックを実行します。";
Blockly.Msg["CONTROLS_IF_TOOLTIP_3"] = "最初の値が true の場合は、最初のステートメントのブロックを実行します。それ以外の場合で、2番目の値が true の場合は、2番目のステートメントのブロックを実行します。";
Blockly.Msg["CONTROLS_IF_TOOLTIP_4"] = "最初の値が true の場合は、最初のステートメントのブロックを実行します。それ以外の場合で、2番目の値が true の場合は、2番目のステートメントのブロックを実行します。すべての値が true でない場合は、最後のステートメントのブロックを実行します。";
Blockly.Msg["CONTROLS_REPEAT_HELPURL"] = "https://ja.wikipedia.org/wiki/for文";
Blockly.Msg["CONTROLS_REPEAT_INPUT_DO"] = "実行";
Blockly.Msg["CONTROLS_REPEAT_TITLE"] = "%1 回繰り返す";
Blockly.Msg["CONTROLS_REPEAT_TOOLTIP"] = "いくつかのステートメントを数回実行します。";
Blockly.Msg["CONTROLS_WHILEUNTIL_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#repeat";  // untranslated
Blockly.Msg["CONTROLS_WHILEUNTIL_OPERATOR_UNTIL"] = "繰り返す：終わる条件";
Blockly.Msg["CONTROLS_WHILEUNTIL_OPERATOR_WHILE"] = "繰り返す：続ける条件";
Blockly.Msg["CONTROLS_WHILEUNTIL_TOOLTIP_UNTIL"] = "値がfalseの間、いくつかのステートメントを実行する。";
Blockly.Msg["CONTROLS_WHILEUNTIL_TOOLTIP_WHILE"] = "値がtrueの間、いくつかのステートメントを実行する。";
Blockly.Msg["DELETE_ALL_BLOCKS"] = "%1個あるすべてのブロックを削除しますか？";
Blockly.Msg["DELETE_BLOCK"] = "ブロックを削除";
Blockly.Msg["DELETE_VARIABLE"] = "変数 '%1' を削除";
Blockly.Msg["DELETE_VARIABLE_CONFIRMATION"] = "%1か所で使われている変数 '%2' を削除しますか？";
Blockly.Msg["DELETE_X_BLOCKS"] = "%1個のブロックを削除";
Blockly.Msg["DIALOG_CANCEL"] = "キャンセル";
Blockly.Msg["DIALOG_OK"] = "OK";
Blockly.Msg["DISABLE_BLOCK"] = "ブロックを無効にする";
Blockly.Msg["DUPLICATE_BLOCK"] = "複製";
Blockly.Msg["DUPLICATE_COMMENT"] = "コメントを複製";
Blockly.Msg["ENABLE_BLOCK"] = "ブロックを有効にする";
Blockly.Msg["EXPAND_ALL"] = "ブロックを展開する";
Blockly.Msg["EXPAND_BLOCK"] = "ブロックを展開する";
Blockly.Msg["EXTERNAL_INPUTS"] = "外部入力";
Blockly.Msg["HELP"] = "ヘルプ";
Blockly.Msg["INLINE_INPUTS"] = "インライン入力";
Blockly.Msg["LISTS_CREATE_EMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-empty-list";  // untranslated
Blockly.Msg["LISTS_CREATE_EMPTY_TITLE"] = "空のリストを作成";
Blockly.Msg["LISTS_CREATE_EMPTY_TOOLTIP"] = "長さ０でデータ・レコードを含まない空のリストを返す";
Blockly.Msg["LISTS_CREATE_WITH_CONTAINER_TITLE_ADD"] = "リスト";
Blockly.Msg["LISTS_CREATE_WITH_CONTAINER_TOOLTIP"] = "追加、削除、またはセクションの順序変更をして、このリスト・ブロックを再構成する。";
Blockly.Msg["LISTS_CREATE_WITH_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-list-with";  // untranslated
Blockly.Msg["LISTS_CREATE_WITH_INPUT_WITH"] = "以下を使ってリストを作成：";
Blockly.Msg["LISTS_CREATE_WITH_ITEM_TOOLTIP"] = "リストに項目を追加。";
Blockly.Msg["LISTS_CREATE_WITH_TOOLTIP"] = "項目数が不定のリストを作成。";
Blockly.Msg["LISTS_GET_INDEX_FIRST"] = "最初";
Blockly.Msg["LISTS_GET_INDEX_FROM_END"] = "位置：後ろから";
Blockly.Msg["LISTS_GET_INDEX_FROM_START"] = "#";
Blockly.Msg["LISTS_GET_INDEX_GET"] = "取得";
Blockly.Msg["LISTS_GET_INDEX_GET_REMOVE"] = "取得して削除";
Blockly.Msg["LISTS_GET_INDEX_LAST"] = "最後";
Blockly.Msg["LISTS_GET_INDEX_RANDOM"] = "ランダム";
Blockly.Msg["LISTS_GET_INDEX_REMOVE"] = "削除";
Blockly.Msg["LISTS_GET_INDEX_TAIL"] = "";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_FIRST"] = "リストの最初の項目を返します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_FROM"] = "リスト内の指定位置にある項目を返します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_LAST"] = "リストの最後の項目を返します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_RANDOM"] = "ランダム アイテム リストを返します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_FIRST"] = "リスト内の最初の項目を削除し返します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_FROM"] = "リスト内の指定位置にある項目を削除し、返します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_LAST"] = "リスト内の最後の項目を削除したあと返します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_RANDOM"] = "リストのランダムなアイテムを削除し返します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_FIRST"] = "リスト内の最初の項目を削除します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_FROM"] = "リスト内の指定された項目を削除します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_LAST"] = "リスト内の最後の項目を削除します。";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_RANDOM"] = "リスト内にあるアイテムをランダムに削除します。";
Blockly.Msg["LISTS_GET_SUBLIST_END_FROM_END"] = "終了位置：後ろから";
Blockly.Msg["LISTS_GET_SUBLIST_END_FROM_START"] = "終了位置：";
Blockly.Msg["LISTS_GET_SUBLIST_END_LAST"] = "最後まで";
Blockly.Msg["LISTS_GET_SUBLIST_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#getting-a-sublist";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_START_FIRST"] = "最初からサブリストを取得する。";
Blockly.Msg["LISTS_GET_SUBLIST_START_FROM_END"] = "端から #のサブリストを取得します。";
Blockly.Msg["LISTS_GET_SUBLIST_START_FROM_START"] = "# からサブディレクトリのリストを取得します。";
Blockly.Msg["LISTS_GET_SUBLIST_TAIL"] = "";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_TOOLTIP"] = "リストの指定された部分のコピーを作成します。";
Blockly.Msg["LISTS_INDEX_FROM_END_TOOLTIP"] = "%1 は、最後の項目です。";
Blockly.Msg["LISTS_INDEX_FROM_START_TOOLTIP"] = "%1 は、最初の項目です。";
Blockly.Msg["LISTS_INDEX_OF_FIRST"] = "で以下のアイテムの最初の出現箇所を検索：";
Blockly.Msg["LISTS_INDEX_OF_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#getting-items-from-a-list";  // untranslated
Blockly.Msg["LISTS_INDEX_OF_LAST"] = "で以下のテキストの最後の出現箇所を検索：";
Blockly.Msg["LISTS_INDEX_OF_TOOLTIP"] = "リスト項目の最初/最後に出現するインデックス位置を返します。項目が見つからない場合は %1 を返します。";
Blockly.Msg["LISTS_INLIST"] = "リスト";
Blockly.Msg["LISTS_ISEMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#is-empty";  // untranslated
Blockly.Msg["LISTS_ISEMPTY_TITLE"] = "%1が空";
Blockly.Msg["LISTS_ISEMPTY_TOOLTIP"] = "リストが空の場合は、true を返します。";
Blockly.Msg["LISTS_LENGTH_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#length-of";  // untranslated
Blockly.Msg["LISTS_LENGTH_TITLE"] = "%1の長さ";
Blockly.Msg["LISTS_LENGTH_TOOLTIP"] = "リストの長さを返します。";
Blockly.Msg["LISTS_REPEAT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-list-with";  // untranslated
Blockly.Msg["LISTS_REPEAT_TITLE"] = "項目%1を%2回繰り返したリストを作成";
Blockly.Msg["LISTS_REPEAT_TOOLTIP"] = "与えられた値を指定された回数繰り返してリストを作成。";
Blockly.Msg["LISTS_REVERSE_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#reversing-a-list";  // untranslated
Blockly.Msg["LISTS_REVERSE_MESSAGE0"] = "%1を逆順に";
Blockly.Msg["LISTS_REVERSE_TOOLTIP"] = "リストのコピーを逆順にする。";
Blockly.Msg["LISTS_SET_INDEX_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#in-list--set";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_INPUT_TO"] = "値：";
Blockly.Msg["LISTS_SET_INDEX_INSERT"] = "挿入位置：";
Blockly.Msg["LISTS_SET_INDEX_SET"] = "セット";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_FIRST"] = "リストの先頭に項目を挿入します。";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_FROM"] = "リスト内の指定位置に項目を挿入します。";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_LAST"] = "リストの末尾に項目を追加します。";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_RANDOM"] = "リストに項目をランダムに挿入します。";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_FIRST"] = "リスト内に最初の項目を設定します。";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_FROM"] = "リスト内の指定された位置に項目を設定します。";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_LAST"] = "リスト内の最後の項目を設定します。";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_RANDOM"] = "リスト内にランダムなアイテムを設定します。";
Blockly.Msg["LISTS_SORT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#sorting-a-list";  // untranslated
Blockly.Msg["LISTS_SORT_ORDER_ASCENDING"] = "昇順";
Blockly.Msg["LISTS_SORT_ORDER_DESCENDING"] = "降順";
Blockly.Msg["LISTS_SORT_TITLE"] = "%1 ( %2 ) に %3 を並び替える";
Blockly.Msg["LISTS_SORT_TOOLTIP"] = "リストのコピーを並べ替え";
Blockly.Msg["LISTS_SORT_TYPE_IGNORECASE"] = "アルファベット順（大文字・小文字の区別無し）";
Blockly.Msg["LISTS_SORT_TYPE_NUMERIC"] = "数値順";
Blockly.Msg["LISTS_SORT_TYPE_TEXT"] = "アルファベット順";
Blockly.Msg["LISTS_SPLIT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#splitting-strings-and-joining-lists";  // untranslated
Blockly.Msg["LISTS_SPLIT_LIST_FROM_TEXT"] = "テキストからリストを作る";
Blockly.Msg["LISTS_SPLIT_TEXT_FROM_LIST"] = "リストからテキストを作る";
Blockly.Msg["LISTS_SPLIT_TOOLTIP_JOIN"] = "テキストのリストを区切り記号で区切られた一つのテキストにする";
Blockly.Msg["LISTS_SPLIT_TOOLTIP_SPLIT"] = "テキストを区切り記号で分割したリストにする";
Blockly.Msg["LISTS_SPLIT_WITH_DELIMITER"] = "区切り記号";
Blockly.Msg["LOGIC_BOOLEAN_FALSE"] = "false";
Blockly.Msg["LOGIC_BOOLEAN_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#values";  // untranslated
Blockly.Msg["LOGIC_BOOLEAN_TOOLTIP"] = "true または false を返します。";
Blockly.Msg["LOGIC_BOOLEAN_TRUE"] = "true";
Blockly.Msg["LOGIC_COMPARE_HELPURL"] = "https://ja.wikipedia.org/wiki/不等式";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_EQ"] = "両方の入力が互いに等しい場合に true を返します。";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_GT"] = "最初の入力が 2 番目の入力よりも大きい場合は true を返します。";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_GTE"] = "最初の入力が 2 番目の入力以上の場合に true を返します。";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_LT"] = "最初の入力が 2 番目の入力よりも小さい場合は true を返します。";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_LTE"] = "最初の入力が 2 番目の入力以下の場合に true を返します。";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_NEQ"] = "両方の入力が互いに等しくない場合に true を返します。";
Blockly.Msg["LOGIC_NEGATE_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#not";  // untranslated
Blockly.Msg["LOGIC_NEGATE_TITLE"] = "%1ではない";
Blockly.Msg["LOGIC_NEGATE_TOOLTIP"] = "入力が false の場合は、true を返します。入力が true の場合は false を返します。";
Blockly.Msg["LOGIC_NULL"] = "null";
Blockly.Msg["LOGIC_NULL_HELPURL"] = "https://en.wikipedia.org/wiki/Nullable_type";  // untranslated
Blockly.Msg["LOGIC_NULL_TOOLTIP"] = "null を返します。";
Blockly.Msg["LOGIC_OPERATION_AND"] = "かつ";
Blockly.Msg["LOGIC_OPERATION_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#logical-operations";  // untranslated
Blockly.Msg["LOGIC_OPERATION_OR"] = "または";
Blockly.Msg["LOGIC_OPERATION_TOOLTIP_AND"] = "両方の入力が true のときに true を返します。";
Blockly.Msg["LOGIC_OPERATION_TOOLTIP_OR"] = "少なくとも 1 つの入力が true のときに true を返します。";
Blockly.Msg["LOGIC_TERNARY_CONDITION"] = "テスト";
Blockly.Msg["LOGIC_TERNARY_HELPURL"] = "https://ja.wikipedia.org/wiki/%3F:";
Blockly.Msg["LOGIC_TERNARY_IF_FALSE"] = "false の場合";
Blockly.Msg["LOGIC_TERNARY_IF_TRUE"] = "true の場合";
Blockly.Msg["LOGIC_TERNARY_TOOLTIP"] = "'テスト' の条件をチェックします。条件が true の場合、'true' の値を返します。それ以外の場合 'false' のを返します。";
Blockly.Msg["MATH_ADDITION_SYMBOL"] = "+";  // untranslated
Blockly.Msg["MATH_ARITHMETIC_HELPURL"] = "https://ja.wikipedia.org/wiki/算術";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_ADD"] = "2 つの数の合計を返します。";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_DIVIDE"] = "2 つの数の商を返します。";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_MINUS"] = "2 つの数の差を返します。";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_MULTIPLY"] = "2 つの数の積を返します。";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_POWER"] = "最初の数を2 番目の値で累乗した結果を返します。";
Blockly.Msg["MATH_ATAN2_HELPURL"] = "https://ja.wikipedia.org/wiki/Atan2";
Blockly.Msg["MATH_ATAN2_TITLE"] = "X:%1 Y:%2のatan2";
Blockly.Msg["MATH_ATAN2_TOOLTIP"] = "アークタンジェントを用いて、点 (X, Y) の角度を -180度から 180度で返します。";
Blockly.Msg["MATH_CHANGE_HELPURL"] = "https://ja.wikipedia.org/wiki/加法";
Blockly.Msg["MATH_CHANGE_TITLE"] = "%1 を %2 増やす";
Blockly.Msg["MATH_CHANGE_TOOLTIP"] = "変数'%1'に数をたす。";
Blockly.Msg["MATH_CONSTANT_HELPURL"] = "https://ja.wikipedia.org/wiki/数学定数";
Blockly.Msg["MATH_CONSTANT_TOOLTIP"] = "いずれかの共通の定数のを返す: π (3.141…), e (2.718…), φ (1.618…), sqrt(2) (1.414…), sqrt(½) (0.707…), or ∞ (無限).";
Blockly.Msg["MATH_CONSTRAIN_HELPURL"] = "https://en.wikipedia.org/wiki/Clamping_(graphics)";  // untranslated
Blockly.Msg["MATH_CONSTRAIN_TITLE"] = "%1 を %2 以上 %3 以下の範囲に制限";
Blockly.Msg["MATH_CONSTRAIN_TOOLTIP"] = "指定した上限と下限の間に値を制限する（上限と下限の値を含む）。";
Blockly.Msg["MATH_DIVISION_SYMBOL"] = "÷";  // untranslated
Blockly.Msg["MATH_IS_DIVISIBLE_BY"] = "は以下で割りきれる：";
Blockly.Msg["MATH_IS_EVEN"] = "は偶数";
Blockly.Msg["MATH_IS_NEGATIVE"] = "は負";
Blockly.Msg["MATH_IS_ODD"] = "は奇数";
Blockly.Msg["MATH_IS_POSITIVE"] = "は正";
Blockly.Msg["MATH_IS_PRIME"] = "は素数";
Blockly.Msg["MATH_IS_TOOLTIP"] = "数字が、偶数、奇数、素数、整数、正数、負数、または特定の数で割り切れるかどうかを判定し、true か false を返します。";
Blockly.Msg["MATH_IS_WHOLE"] = "は整数";
Blockly.Msg["MATH_MODULO_HELPURL"] = "https://ja.wikipedia.org/wiki/剰余演算";
Blockly.Msg["MATH_MODULO_TITLE"] = "%1÷%2の余り";
Blockly.Msg["MATH_MODULO_TOOLTIP"] = "2つの数値の割り算の余りを返す。";
Blockly.Msg["MATH_MULTIPLICATION_SYMBOL"] = "×";  // untranslated
Blockly.Msg["MATH_NUMBER_HELPURL"] = "https://ja.wikipedia.org/wiki/数";
Blockly.Msg["MATH_NUMBER_TOOLTIP"] = "数です。";
Blockly.Msg["MATH_ONLIST_HELPURL"] = "";  // untranslated
Blockly.Msg["MATH_ONLIST_OPERATOR_AVERAGE"] = "リストの平均";
Blockly.Msg["MATH_ONLIST_OPERATOR_MAX"] = "リストの最大値";
Blockly.Msg["MATH_ONLIST_OPERATOR_MEDIAN"] = "リストの中央値";
Blockly.Msg["MATH_ONLIST_OPERATOR_MIN"] = "リストの最小値";
Blockly.Msg["MATH_ONLIST_OPERATOR_MODE"] = "リストの最頻値";
Blockly.Msg["MATH_ONLIST_OPERATOR_RANDOM"] = "リストからランダムに選ばれた項目";
Blockly.Msg["MATH_ONLIST_OPERATOR_STD_DEV"] = "リストの標準偏差";
Blockly.Msg["MATH_ONLIST_OPERATOR_SUM"] = "リストの合計";
Blockly.Msg["MATH_ONLIST_TOOLTIP_AVERAGE"] = "リストの数値の平均 (算術平均) を返す。";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MAX"] = "リストの最大値を返す。";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MEDIAN"] = "リストの中央値を返す。";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MIN"] = "リストの最小値を返す。";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MODE"] = "リスト中の最頻項目のリストを返す。";
Blockly.Msg["MATH_ONLIST_TOOLTIP_RANDOM"] = "リストからランダムに選ばれた要素を返す。";
Blockly.Msg["MATH_ONLIST_TOOLTIP_STD_DEV"] = "リストの標準偏差を返す。";
Blockly.Msg["MATH_ONLIST_TOOLTIP_SUM"] = "リストの数値を足して返す。";
Blockly.Msg["MATH_POWER_SYMBOL"] = "^";  // untranslated
Blockly.Msg["MATH_RANDOM_FLOAT_HELPURL"] = "https://ja.wikipedia.org/wiki/疑似乱数";
Blockly.Msg["MATH_RANDOM_FLOAT_TITLE_RANDOM"] = "1未満の正の乱数";
Blockly.Msg["MATH_RANDOM_FLOAT_TOOLTIP"] = "0.0以上で1.0未満の範囲の乱数を返します。";
Blockly.Msg["MATH_RANDOM_INT_HELPURL"] = "https://ja.wikipedia.org/wiki/疑似乱数";
Blockly.Msg["MATH_RANDOM_INT_TITLE"] = "%1から%2までのランダムな整数";
Blockly.Msg["MATH_RANDOM_INT_TOOLTIP"] = "指定された（上下限を含む）範囲のランダムな整数を返します。";
Blockly.Msg["MATH_ROUND_HELPURL"] = "https://ja.wikipedia.org/wiki/端数処理";
Blockly.Msg["MATH_ROUND_OPERATOR_ROUND"] = "四捨五入";
Blockly.Msg["MATH_ROUND_OPERATOR_ROUNDDOWN"] = "切り捨て";
Blockly.Msg["MATH_ROUND_OPERATOR_ROUNDUP"] = "切り上げ";
Blockly.Msg["MATH_ROUND_TOOLTIP"] = "数値を切り上げるか切り捨てる";
Blockly.Msg["MATH_SINGLE_HELPURL"] = "https://ja.wikipedia.org/wiki/平方根";
Blockly.Msg["MATH_SINGLE_OP_ABSOLUTE"] = "絶対値";
Blockly.Msg["MATH_SINGLE_OP_ROOT"] = "平方根";
Blockly.Msg["MATH_SINGLE_TOOLTIP_ABS"] = "絶対値を返す。";
Blockly.Msg["MATH_SINGLE_TOOLTIP_EXP"] = "ネイピア数eの数値乗を返す。";
Blockly.Msg["MATH_SINGLE_TOOLTIP_LN"] = "数値の自然対数を返す。";
Blockly.Msg["MATH_SINGLE_TOOLTIP_LOG10"] = "底が10の対数を返す。";
Blockly.Msg["MATH_SINGLE_TOOLTIP_NEG"] = "負の数を返す。";
Blockly.Msg["MATH_SINGLE_TOOLTIP_POW10"] = "10の数値乗を返す。";
Blockly.Msg["MATH_SINGLE_TOOLTIP_ROOT"] = "平方根を返す。";
Blockly.Msg["MATH_SUBTRACTION_SYMBOL"] = "-";  // untranslated
Blockly.Msg["MATH_TRIG_ACOS"] = "acos";
Blockly.Msg["MATH_TRIG_ASIN"] = "asin";
Blockly.Msg["MATH_TRIG_ATAN"] = "atan";
Blockly.Msg["MATH_TRIG_COS"] = "cos";
Blockly.Msg["MATH_TRIG_HELPURL"] = "https://ja.wikipedia.org/wiki/三角関数";
Blockly.Msg["MATH_TRIG_SIN"] = "sin";
Blockly.Msg["MATH_TRIG_TAN"] = "tan";
Blockly.Msg["MATH_TRIG_TOOLTIP_ACOS"] = "アークコサイン（arccosin）を返す。";
Blockly.Msg["MATH_TRIG_TOOLTIP_ASIN"] = "アークサイン（arcsin）を返す。";
Blockly.Msg["MATH_TRIG_TOOLTIP_ATAN"] = "アークタンジェント（arctan）を返す。";
Blockly.Msg["MATH_TRIG_TOOLTIP_COS"] = "（ラジアンではなく）度数の余弦（cosin）を返す。";
Blockly.Msg["MATH_TRIG_TOOLTIP_SIN"] = "（ラジアンではなく）度数の正弦（sin）を返す。";
Blockly.Msg["MATH_TRIG_TOOLTIP_TAN"] = "（ラジアンではなく）度数の正接（tan）を返す。";
Blockly.Msg["NEW_COLOUR_VARIABLE"] = "色の変数を作る...";
Blockly.Msg["NEW_NUMBER_VARIABLE"] = "数の変数を作る...";
Blockly.Msg["NEW_STRING_VARIABLE"] = "文字列の変数を作る...";
Blockly.Msg["NEW_VARIABLE"] = "変数の作成…";
Blockly.Msg["NEW_VARIABLE_TITLE"] = "新しい変数の名前:";
Blockly.Msg["NEW_VARIABLE_TYPE_TITLE"] = "新しい変数の型:";
Blockly.Msg["ORDINAL_NUMBER_SUFFIX"] = "";  // untranslated
Blockly.Msg["PROCEDURES_ALLOW_STATEMENTS"] = "ステートメントを許可";
Blockly.Msg["PROCEDURES_BEFORE_PARAMS"] = "引数：";
Blockly.Msg["PROCEDURES_CALLNORETURN_HELPURL"] = "https://ja.wikipedia.org/wiki/サブルーチン";
Blockly.Msg["PROCEDURES_CALLNORETURN_TOOLTIP"] = "ユーザー定義関数 '%1' を実行します。";
Blockly.Msg["PROCEDURES_CALLRETURN_HELPURL"] = "https://ja.wikipedia.org/wiki/サブルーチン";
Blockly.Msg["PROCEDURES_CALLRETURN_TOOLTIP"] = "ユーザー定義関数 '%1' を実行し、その出力を使用します。";
Blockly.Msg["PROCEDURES_CALL_BEFORE_PARAMS"] = "引数：";
Blockly.Msg["PROCEDURES_CREATE_DO"] = "'%1' を作成";
Blockly.Msg["PROCEDURES_DEFNORETURN_COMMENT"] = "この関数の説明…";
Blockly.Msg["PROCEDURES_DEFNORETURN_DO"] = "";  // untranslated
Blockly.Msg["PROCEDURES_DEFNORETURN_HELPURL"] = "https://en.wikipedia.org/wiki/Subroutine";  // untranslated
Blockly.Msg["PROCEDURES_DEFNORETURN_PROCEDURE"] = "何かする";
Blockly.Msg["PROCEDURES_DEFNORETURN_TITLE"] = "関数";
Blockly.Msg["PROCEDURES_DEFNORETURN_TOOLTIP"] = "出力なしの関数を作成します。";
Blockly.Msg["PROCEDURES_DEFRETURN_HELPURL"] = "https://en.wikipedia.org/wiki/Subroutine";  // untranslated
Blockly.Msg["PROCEDURES_DEFRETURN_RETURN"] = "返す";
Blockly.Msg["PROCEDURES_DEFRETURN_TOOLTIP"] = "一つの出力を持つ関数を作成します。";
Blockly.Msg["PROCEDURES_DEF_DUPLICATE_WARNING"] = "警告: この関数には重複するパラメーターがあります。";
Blockly.Msg["PROCEDURES_HIGHLIGHT_DEF"] = "関数の内容を強調表示します。";
Blockly.Msg["PROCEDURES_IFRETURN_HELPURL"] = "http://c2.com/cgi/wiki?GuardClause";  // untranslated
Blockly.Msg["PROCEDURES_IFRETURN_TOOLTIP"] = "1番目の値が true の場合、2番目の値を返します。";
Blockly.Msg["PROCEDURES_IFRETURN_WARNING"] = "警告: このブロックは、関数定義内でのみ使用できます。";
Blockly.Msg["PROCEDURES_MUTATORARG_TITLE"] = "入力名:";
Blockly.Msg["PROCEDURES_MUTATORARG_TOOLTIP"] = "関数への入力の追加。";
Blockly.Msg["PROCEDURES_MUTATORCONTAINER_TITLE"] = "入力";
Blockly.Msg["PROCEDURES_MUTATORCONTAINER_TOOLTIP"] = "この関数への入力の追加、削除、順番変更。";
Blockly.Msg["REDO"] = "やり直す";
Blockly.Msg["REMOVE_COMMENT"] = "コメントを削除";
Blockly.Msg["RENAME_VARIABLE"] = "変数の名前を変える…";
Blockly.Msg["RENAME_VARIABLE_TITLE"] = "選択した%1個すべての変数の名前を変える：";
Blockly.Msg["TEXT_APPEND_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-modification";  // untranslated
Blockly.Msg["TEXT_APPEND_TITLE"] = "項目 %1 へテキストを追加 %2";
Blockly.Msg["TEXT_APPEND_TOOLTIP"] = "変数 '%1' にテキストを追加。";
Blockly.Msg["TEXT_CHANGECASE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#adjusting-text-case";  // untranslated
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_LOWERCASE"] = "小文字に";
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_TITLECASE"] = "タイトル ケースに";
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_UPPERCASE"] = "大文字に";
Blockly.Msg["TEXT_CHANGECASE_TOOLTIP"] = "別のケースに、テキストのコピーを返します。";
Blockly.Msg["TEXT_CHARAT_FIRST"] = "最初の文字を得る";
Blockly.Msg["TEXT_CHARAT_FROM_END"] = "の、後ろから以下の数字番目の文字：";
Blockly.Msg["TEXT_CHARAT_FROM_START"] = "の、以下の数字番目の文字：";
Blockly.Msg["TEXT_CHARAT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#extracting-text";  // untranslated
Blockly.Msg["TEXT_CHARAT_LAST"] = "最後の文字を得る";
Blockly.Msg["TEXT_CHARAT_RANDOM"] = "ランダムな文字を得る";
Blockly.Msg["TEXT_CHARAT_TAIL"] = "";  // untranslated
Blockly.Msg["TEXT_CHARAT_TITLE"] = "テキスト %1 %2";
Blockly.Msg["TEXT_CHARAT_TOOLTIP"] = "指定された位置に文字を返します。";
Blockly.Msg["TEXT_COUNT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#counting-substrings";  // untranslated
Blockly.Msg["TEXT_COUNT_MESSAGE0"] = "%2に含まれる%1の数を数える";
Blockly.Msg["TEXT_COUNT_TOOLTIP"] = "とある文が別の文のなかに使われた回数を数える。";
Blockly.Msg["TEXT_CREATE_JOIN_ITEM_TOOLTIP"] = "テキストへ項目を追加。";
Blockly.Msg["TEXT_CREATE_JOIN_TITLE_JOIN"] = "結合";
Blockly.Msg["TEXT_CREATE_JOIN_TOOLTIP"] = "セクションを追加、削除、または順序変更して、ブロックを再構成。";
Blockly.Msg["TEXT_GET_SUBSTRING_END_FROM_END"] = "終了位置：後ろから";
Blockly.Msg["TEXT_GET_SUBSTRING_END_FROM_START"] = "終了位置：";
Blockly.Msg["TEXT_GET_SUBSTRING_END_LAST"] = "最後の文字";
Blockly.Msg["TEXT_GET_SUBSTRING_HELPURL"] = "https://github.com/google/blockly/wiki/Text#extracting-a-region-of-text";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_INPUT_IN_TEXT"] = "テキスト";
Blockly.Msg["TEXT_GET_SUBSTRING_START_FIRST"] = "の部分文字列を取得；最初から";
Blockly.Msg["TEXT_GET_SUBSTRING_START_FROM_END"] = "の部分文字列を取得；開始位置：後ろから";
Blockly.Msg["TEXT_GET_SUBSTRING_START_FROM_START"] = "の部分文字列を取得；開始位置：";
Blockly.Msg["TEXT_GET_SUBSTRING_TAIL"] = "";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_TOOLTIP"] = "テキストの指定部分を返します。";
Blockly.Msg["TEXT_INDEXOF_HELPURL"] = "https://github.com/google/blockly/wiki/Text#finding-text";  // untranslated
Blockly.Msg["TEXT_INDEXOF_OPERATOR_FIRST"] = "で以下のテキストの最初の出現箇所を検索：";
Blockly.Msg["TEXT_INDEXOF_OPERATOR_LAST"] = "で以下のテキストの最後の出現箇所を検索：";
Blockly.Msg["TEXT_INDEXOF_TITLE"] = "テキスト %1 %2 %3";
Blockly.Msg["TEXT_INDEXOF_TOOLTIP"] = "二番目のテキストの中で一番目のテキストが最初／最後に出現したインデックスを返す。テキストが見つからない場合は%1を返す。";
Blockly.Msg["TEXT_ISEMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Text#checking-for-empty-text";  // untranslated
Blockly.Msg["TEXT_ISEMPTY_TITLE"] = "%1が空";
Blockly.Msg["TEXT_ISEMPTY_TOOLTIP"] = "与えられたテキストが空の場合は true を返す。";
Blockly.Msg["TEXT_JOIN_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-creation";  // untranslated
Blockly.Msg["TEXT_JOIN_TITLE_CREATEWITH"] = "テキストを結合して作成：";
Blockly.Msg["TEXT_JOIN_TOOLTIP"] = "任意の数の項目一部を一緒に接合してテキストを作成。";
Blockly.Msg["TEXT_LENGTH_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-modification";  // untranslated
Blockly.Msg["TEXT_LENGTH_TITLE"] = "%1の長さ";
Blockly.Msg["TEXT_LENGTH_TOOLTIP"] = "与えられたテキストの(スペースを含む)文字数を返す。";
Blockly.Msg["TEXT_PRINT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#printing-text";  // untranslated
Blockly.Msg["TEXT_PRINT_TITLE"] = "%1 を表示";
Blockly.Msg["TEXT_PRINT_TOOLTIP"] = "指定したテキスト、番号または他の値を印刷します。";
Blockly.Msg["TEXT_PROMPT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#getting-input-from-the-user";  // untranslated
Blockly.Msg["TEXT_PROMPT_TOOLTIP_NUMBER"] = "ユーザーに数値のインプットを求める。";
Blockly.Msg["TEXT_PROMPT_TOOLTIP_TEXT"] = "ユーザーにテキスト入力を求める。";
Blockly.Msg["TEXT_PROMPT_TYPE_NUMBER"] = "メッセージで番号の入力を求める";
Blockly.Msg["TEXT_PROMPT_TYPE_TEXT"] = "メッセージでテキスト入力を求める";
Blockly.Msg["TEXT_REPLACE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#replacing-substrings";  // untranslated
Blockly.Msg["TEXT_REPLACE_MESSAGE0"] = "%3に含まれる%1を%2に置換";
Blockly.Msg["TEXT_REPLACE_TOOLTIP"] = "文に含まれるキーワードを置換する。";
Blockly.Msg["TEXT_REVERSE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#reversing-text";  // untranslated
Blockly.Msg["TEXT_REVERSE_MESSAGE0"] = "%1を逆順に";
Blockly.Msg["TEXT_REVERSE_TOOLTIP"] = "文の文字を逆順にする。";
Blockly.Msg["TEXT_TEXT_HELPURL"] = "https://ja.wikipedia.org/wiki/文字列";
Blockly.Msg["TEXT_TEXT_TOOLTIP"] = "文字、単語、または行のテキスト。";
Blockly.Msg["TEXT_TRIM_HELPURL"] = "https://github.com/google/blockly/wiki/Text#trimming-removing-spaces";  // untranslated
Blockly.Msg["TEXT_TRIM_OPERATOR_BOTH"] = "両端のスペースを取り除く";
Blockly.Msg["TEXT_TRIM_OPERATOR_LEFT"] = "左端のスペースを取り除く";
Blockly.Msg["TEXT_TRIM_OPERATOR_RIGHT"] = "右端のスペースを取り除く";
Blockly.Msg["TEXT_TRIM_TOOLTIP"] = "スペースを 1 つまたは両方の端から削除したのち、テキストのコピーを返します。";
Blockly.Msg["TODAY"] = "今日";
Blockly.Msg["UNDO"] = "取り消す";
Blockly.Msg["UNNAMED_KEY"] = "名前なし";
Blockly.Msg["VARIABLES_DEFAULT_NAME"] = "項目";
Blockly.Msg["VARIABLES_GET_CREATE_SET"] = "'セット%1を作成します。";
Blockly.Msg["VARIABLES_GET_HELPURL"] = "https://github.com/google/blockly/wiki/Variables#get";  // untranslated
Blockly.Msg["VARIABLES_GET_TOOLTIP"] = "この変数の値を返します。";
Blockly.Msg["VARIABLES_SET"] = "%1 に %2 をセット";
Blockly.Msg["VARIABLES_SET_CREATE_GET"] = "'%1 を取得' を作成します。";
Blockly.Msg["VARIABLES_SET_HELPURL"] = "https://github.com/google/blockly/wiki/Variables#set";  // untranslated
Blockly.Msg["VARIABLES_SET_TOOLTIP"] = "この入力を変数と等しくなるように設定します。";
Blockly.Msg["VARIABLE_ALREADY_EXISTS"] = "変数名 '%1' は既に存在しています。";
Blockly.Msg["VARIABLE_ALREADY_EXISTS_FOR_ANOTHER_TYPE"] = "'%2' 型の '%1' という名前の変数が既に存在します。";
Blockly.Msg["WORKSPACE_ARIA_LABEL"] = "Blocklyワークスペース";
Blockly.Msg["WORKSPACE_COMMENT_DEFAULT_TEXT"] = "ここへ入力";
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
