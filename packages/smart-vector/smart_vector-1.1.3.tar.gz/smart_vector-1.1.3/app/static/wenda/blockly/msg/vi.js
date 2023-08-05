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

Blockly.Msg["ADD_COMMENT"] = "Thêm Chú Giải";
Blockly.Msg["CANNOT_DELETE_VARIABLE_PROCEDURE"] = "Không thể xóa giá trị '%1' vì nó được bao gồm trong định nghĩa của chức năng '%2'";
Blockly.Msg["CHANGE_VALUE_TITLE"] = "Thay giá trị thành:";
Blockly.Msg["CLEAN_UP"] = "Sắp xếp lại các khối";
Blockly.Msg["COLLAPSED_WARNINGS_WARNING"] = "Các khối bị sập có chứa cảnh báo.";
Blockly.Msg["COLLAPSE_ALL"] = "Thu Nhỏ Mọi Mảnh";
Blockly.Msg["COLLAPSE_BLOCK"] = "Thu Nhỏ Mảnh";
Blockly.Msg["COLOUR_BLEND_COLOUR1"] = "màu 1";
Blockly.Msg["COLOUR_BLEND_COLOUR2"] = "màu 2";
Blockly.Msg["COLOUR_BLEND_HELPURL"] = "https://meyerweb.com/eric/tools/color-blend/#:::rgbp";  // untranslated
Blockly.Msg["COLOUR_BLEND_RATIO"] = "tỉ lệ";
Blockly.Msg["COLOUR_BLEND_TITLE"] = "pha";
Blockly.Msg["COLOUR_BLEND_TOOLTIP"] = "Pha hai màu với nhau theo tỉ lệ (0 - 100).";
Blockly.Msg["COLOUR_PICKER_HELPURL"] = "https://vi.wikipedia.org/wiki/M%C3%A0u_s%E1%BA%AFc";
Blockly.Msg["COLOUR_PICKER_TOOLTIP"] = "Chọn một màu từ bảng màu.";
Blockly.Msg["COLOUR_RANDOM_HELPURL"] = "http://randomcolour.com";  // untranslated
Blockly.Msg["COLOUR_RANDOM_TITLE"] = "màu bất kỳ";
Blockly.Msg["COLOUR_RANDOM_TOOLTIP"] = "chọn một màu bất kỳ.";
Blockly.Msg["COLOUR_RGB_BLUE"] = "màu xanh dương";
Blockly.Msg["COLOUR_RGB_GREEN"] = "màu xanh lá cây";
Blockly.Msg["COLOUR_RGB_HELPURL"] = "https://www.december.com/html/spec/colorpercompact.html";  // untranslated
Blockly.Msg["COLOUR_RGB_RED"] = "màu đỏ";
Blockly.Msg["COLOUR_RGB_TITLE"] = "tạo màu từ";
Blockly.Msg["COLOUR_RGB_TOOLTIP"] = "Tạo màu từ ba màu: đỏ, xanh lá cây, xanh dương với số lượng cụ thể.  Mỗi số phải có giá trị từ 0 đến 100.";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#loop-termination-blocks";  // untranslated
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_OPERATOR_BREAK"] = "thoát";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_OPERATOR_CONTINUE"] = "sang lần lặp tiếp theo";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_TOOLTIP_BREAK"] = "Thoát khỏi vòng lặp hiện tại.";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_TOOLTIP_CONTINUE"] = "Bỏ qua phần còn lại trong vòng lặp này, và sang lần lặp tiếp theo.";
Blockly.Msg["CONTROLS_FLOW_STATEMENTS_WARNING"] = "Chú ý: Mảnh này chỉ có thế dùng trong các vòng lặp.";
Blockly.Msg["CONTROLS_FOREACH_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#for-each";  // untranslated
Blockly.Msg["CONTROLS_FOREACH_TITLE"] = "với mỗi thành phần %1 trong danh sách %2";
Blockly.Msg["CONTROLS_FOREACH_TOOLTIP"] = "Trong một danh sách, lấy từng thành phần, gán vào biến \"%1\", rồi thực hiện một số lệnh.";
Blockly.Msg["CONTROLS_FOR_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#count-with";  // untranslated
Blockly.Msg["CONTROLS_FOR_TITLE"] = "đếm theo %1 từ %2 đến %3 mỗi lần thêm %4";
Blockly.Msg["CONTROLS_FOR_TOOLTIP"] = "Cho biến '%1' lấy các giá trị từ số bắt đầu đến số kết thúc, đếm theo khoảng thời gian đã chỉ định và thực hiện các khối được chỉ định.";
Blockly.Msg["CONTROLS_IF_ELSEIF_TOOLTIP"] = "Thêm một điều kiện vào mảnh nếu.";
Blockly.Msg["CONTROLS_IF_ELSE_TOOLTIP"] = "Cuối cùng, khi không điều kiện nào đúng.";
Blockly.Msg["CONTROLS_IF_HELPURL"] = "https://github.com/google/blockly/wiki/IfElse";  // untranslated
Blockly.Msg["CONTROLS_IF_IF_TOOLTIP"] = "Thêm, bỏ, hoặc đổi thứ tự các mảnh con để tạo cấu trúc mới cho mảnh nếu.";
Blockly.Msg["CONTROLS_IF_MSG_ELSE"] = "nếu không";
Blockly.Msg["CONTROLS_IF_MSG_ELSEIF"] = "nếu không nếu";
Blockly.Msg["CONTROLS_IF_MSG_IF"] = "nếu";
Blockly.Msg["CONTROLS_IF_TOOLTIP_1"] = "Nếu điều kiện đúng, thực hiện các lệnh.";
Blockly.Msg["CONTROLS_IF_TOOLTIP_2"] = "Nếu điều kiện đúng, thực hiện các lệnh đầu.  Nếu sai, thực hiện các lệnh sau.";
Blockly.Msg["CONTROLS_IF_TOOLTIP_3"] = "Nếu điều kiện đúng, thực hiện các lệnh đầu.  Nếu không, nếu điều kiện thứ hai đúng, thực hiện các lệnh thứ hai.";
Blockly.Msg["CONTROLS_IF_TOOLTIP_4"] = "Nếu điều kiện đúng, thực hiện các lệnh đầu.  Nếu không, nếu điều kiện thứ hai đúng, thực hiện các lệnh thứ hai.  Nếu không điều kiện nào đúng, thực hiện các lệnh cuối cùng.";
Blockly.Msg["CONTROLS_REPEAT_HELPURL"] = "https://en.wikipedia.org/wiki/For_loop";  // untranslated
Blockly.Msg["CONTROLS_REPEAT_INPUT_DO"] = "thực hiện";
Blockly.Msg["CONTROLS_REPEAT_TITLE"] = "lặp lại %1 lần";
Blockly.Msg["CONTROLS_REPEAT_TOOLTIP"] = "Thực hiện các lệnh vài lần.";
Blockly.Msg["CONTROLS_WHILEUNTIL_HELPURL"] = "https://github.com/google/blockly/wiki/Loops#repeat";  // untranslated
Blockly.Msg["CONTROLS_WHILEUNTIL_OPERATOR_UNTIL"] = "lặp lại cho đến khi";
Blockly.Msg["CONTROLS_WHILEUNTIL_OPERATOR_WHILE"] = "lặp lại trong khi";
Blockly.Msg["CONTROLS_WHILEUNTIL_TOOLTIP_UNTIL"] = "Miễn là điều kiện còn sai, thì thực hiện các lệnh.  Khi điều kiện đúng thì ngưng.";
Blockly.Msg["CONTROLS_WHILEUNTIL_TOOLTIP_WHILE"] = "Miễn là điều kiện còn đúng, thì thực hiện các lệnh.";
Blockly.Msg["DELETE_ALL_BLOCKS"] = "Xóa hết %1 mảnh?";
Blockly.Msg["DELETE_BLOCK"] = "Xóa Mảnh Này";
Blockly.Msg["DELETE_VARIABLE"] = "Xóa giá trị '%1'";
Blockly.Msg["DELETE_VARIABLE_CONFIRMATION"] = "Xóa %1 lần dùng của giá trị '%2'?";
Blockly.Msg["DELETE_X_BLOCKS"] = "Xóa %1 Mảnh";
Blockly.Msg["DIALOG_CANCEL"] = "Hủy";
Blockly.Msg["DIALOG_OK"] = "OK";
Blockly.Msg["DISABLE_BLOCK"] = "Ngưng Tác Dụng";
Blockly.Msg["DUPLICATE_BLOCK"] = "Tạo Bản Sao";
Blockly.Msg["DUPLICATE_COMMENT"] = "Bình luận trùng";
Blockly.Msg["ENABLE_BLOCK"] = "Phục Hồi Tác Dụng";
Blockly.Msg["EXPAND_ALL"] = "Mở Lớn Mọi Mảnh";
Blockly.Msg["EXPAND_BLOCK"] = "Mở Lớn Mảnh";
Blockly.Msg["EXTERNAL_INPUTS"] = "Chỗ Gắn Bên Ngoài";
Blockly.Msg["HELP"] = "Trợ Giúp";
Blockly.Msg["INLINE_INPUTS"] = "Chỗ Gắn Cùng Dòng";
Blockly.Msg["LISTS_CREATE_EMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-empty-list";  // untranslated
Blockly.Msg["LISTS_CREATE_EMPTY_TITLE"] = "tạo danh sách trống";
Blockly.Msg["LISTS_CREATE_EMPTY_TOOLTIP"] = "Hoàn trả một danh sách, với độ dài 0, không có thành tố nào cả";
Blockly.Msg["LISTS_CREATE_WITH_CONTAINER_TITLE_ADD"] = "danh sách";
Blockly.Msg["LISTS_CREATE_WITH_CONTAINER_TOOLTIP"] = "Thêm, bỏ, hoặc sắp xếp lại các thành phần để tạo dựng mảnh danh sách này.";
Blockly.Msg["LISTS_CREATE_WITH_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-list-with";  // untranslated
Blockly.Msg["LISTS_CREATE_WITH_INPUT_WITH"] = "tạo danh sách gồm";
Blockly.Msg["LISTS_CREATE_WITH_ITEM_TOOLTIP"] = "Thêm vật vào danh sách.";
Blockly.Msg["LISTS_CREATE_WITH_TOOLTIP"] = "Tạo một danh sách bao gồm nhiều vậts, với một số lượng bất kỳ.";
Blockly.Msg["LISTS_GET_INDEX_FIRST"] = "đầu tiên";
Blockly.Msg["LISTS_GET_INDEX_FROM_END"] = "(đếm từ cuối) thứ";
Blockly.Msg["LISTS_GET_INDEX_FROM_START"] = "thứ";
Blockly.Msg["LISTS_GET_INDEX_GET"] = "lấy thành tố";
Blockly.Msg["LISTS_GET_INDEX_GET_REMOVE"] = "lấy và xóa thành tố";
Blockly.Msg["LISTS_GET_INDEX_LAST"] = "cuối cùng";
Blockly.Msg["LISTS_GET_INDEX_RANDOM"] = "bất kỳ";
Blockly.Msg["LISTS_GET_INDEX_REMOVE"] = "xóa thành tố";
Blockly.Msg["LISTS_GET_INDEX_TAIL"] = "";  // untranslated
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_FIRST"] = "Hoàn trả thành tố đầu tiên trong danh sách.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_FROM"] = "Hoàn trả thành tố trong danh sách ở vị trí ấn định.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_LAST"] = "Hoàn trả thành tố cuối cùng trong danh sách.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_RANDOM"] = "Hoàn trả một thành tố bất kỳ trong danh sách.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_FIRST"] = "Hoàn trả và xóa thành tố đầu tiên trong danh sách.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_FROM"] = "Hoàn trả và xóa thành tố trong danh sách ở vị trí ấn định.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_LAST"] = "Hoàn trả và xóa thành tố cuối cùng trong danh sách.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_GET_REMOVE_RANDOM"] = "Hoàn trả và xóa mộtthành tố bất kỳ trong danh sách.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_FIRST"] = "Xóa thành tố đầu tiên trong danh sách.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_FROM"] = "Xóa thành tố trong danh sách ở vị trí ấn định.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_LAST"] = "Xóa thành tố cuối cùng trong danh sách.";
Blockly.Msg["LISTS_GET_INDEX_TOOLTIP_REMOVE_RANDOM"] = "Xóa thành tố bất kỳ trong danh sách.";
Blockly.Msg["LISTS_GET_SUBLIST_END_FROM_END"] = "đến (đếm từ cuối) thứ";
Blockly.Msg["LISTS_GET_SUBLIST_END_FROM_START"] = "đến thứ";
Blockly.Msg["LISTS_GET_SUBLIST_END_LAST"] = "đến cuối cùng";
Blockly.Msg["LISTS_GET_SUBLIST_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#getting-a-sublist";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_START_FIRST"] = "lấy một danh sách con từ đầu tiên";
Blockly.Msg["LISTS_GET_SUBLIST_START_FROM_END"] = "lấy một danh sách con từ (đếm từ cuối) từ vị trí thứ";
Blockly.Msg["LISTS_GET_SUBLIST_START_FROM_START"] = "lấy một danh sách con từ vị trí thứ";
Blockly.Msg["LISTS_GET_SUBLIST_TAIL"] = "";  // untranslated
Blockly.Msg["LISTS_GET_SUBLIST_TOOLTIP"] = "Lấy một mảng của danh sách này để tạo danh sách con.";
Blockly.Msg["LISTS_INDEX_FROM_END_TOOLTIP"] = "%1 là thành tố cuối cùng.";
Blockly.Msg["LISTS_INDEX_FROM_START_TOOLTIP"] = "%1 là thành tố đầu tiên.";
Blockly.Msg["LISTS_INDEX_OF_FIRST"] = "tìm sự có mặt đầu tiên của vật";
Blockly.Msg["LISTS_INDEX_OF_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#getting-items-from-a-list";  // untranslated
Blockly.Msg["LISTS_INDEX_OF_LAST"] = "tìm sự có mặt cuối cùng của vật";
Blockly.Msg["LISTS_INDEX_OF_TOOLTIP"] = "Hoàn trả vị trí xuất hiện đầu tiên/cuối cùng của vật trong danh sách. Nếu không tìm thấy thì hoàn trả số %1.";
Blockly.Msg["LISTS_INLIST"] = "trong dánh sách";
Blockly.Msg["LISTS_ISEMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#is-empty";  // untranslated
Blockly.Msg["LISTS_ISEMPTY_TITLE"] = "%1 trống rỗng";
Blockly.Msg["LISTS_ISEMPTY_TOOLTIP"] = "Hoàn trả “đúng\" nếu danh sách không có thành tử nào.";
Blockly.Msg["LISTS_LENGTH_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#length-of";  // untranslated
Blockly.Msg["LISTS_LENGTH_TITLE"] = "độ dài của %1";
Blockly.Msg["LISTS_LENGTH_TOOLTIP"] = "Hoàn trả độ dài của một danh sách.";
Blockly.Msg["LISTS_REPEAT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#create-list-with";  // untranslated
Blockly.Msg["LISTS_REPEAT_TITLE"] = "tạo danh sách gồm một vật %1 lặp lại %2 lần";
Blockly.Msg["LISTS_REPEAT_TOOLTIP"] = "Tạo danh sách gồm một số lượng vật nhất định với mỗi vật đều giống nhau.";
Blockly.Msg["LISTS_REVERSE_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#reversing-a-list";  // untranslated
Blockly.Msg["LISTS_REVERSE_MESSAGE0"] = "đảo ngược %1";
Blockly.Msg["LISTS_REVERSE_TOOLTIP"] = "Đảo ngược bản sao chép của một danh sách.";
Blockly.Msg["LISTS_SET_INDEX_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#in-list--set";  // untranslated
Blockly.Msg["LISTS_SET_INDEX_INPUT_TO"] = "giá trị";
Blockly.Msg["LISTS_SET_INDEX_INSERT"] = "chèn vào vị trí";
Blockly.Msg["LISTS_SET_INDEX_SET"] = "đặt";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_FIRST"] = "Chèn vật vào đầu danh sách.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_FROM"] = "Chèn vật vào danh sách theo vị trí ấn định.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_LAST"] = "Gắn thêm vật vào cuối danh sách.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_INSERT_RANDOM"] = "Gắn chèn vật vào danh sách ở vị trí ngẫu nhiên.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_FIRST"] = "Đặt giá trị của thành tố đầu tiên trong danh sách.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_FROM"] = "Đặt giá trị của thành tố ở vị trí ấn định trong một danh sách.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_LAST"] = "Đặt giá trị của thành tố cuối cùng trong danh sách.";
Blockly.Msg["LISTS_SET_INDEX_TOOLTIP_SET_RANDOM"] = "Đặt giá trị của thành tố ngẫu nhiên trong danh sách.";
Blockly.Msg["LISTS_SORT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#sorting-a-list";  // untranslated
Blockly.Msg["LISTS_SORT_ORDER_ASCENDING"] = "tăng dần";
Blockly.Msg["LISTS_SORT_ORDER_DESCENDING"] = "giảm dần";
Blockly.Msg["LISTS_SORT_TITLE"] = "sắp xếp %1 %2 %3";
Blockly.Msg["LISTS_SORT_TOOLTIP"] = "Sắp xếp một bản sao của một danh sách.";
Blockly.Msg["LISTS_SORT_TYPE_IGNORECASE"] = "chữ cái, không phân biệt hoa/thường";
Blockly.Msg["LISTS_SORT_TYPE_NUMERIC"] = "số";
Blockly.Msg["LISTS_SORT_TYPE_TEXT"] = "chữ cái";
Blockly.Msg["LISTS_SPLIT_HELPURL"] = "https://github.com/google/blockly/wiki/Lists#splitting-strings-and-joining-lists";  // untranslated
Blockly.Msg["LISTS_SPLIT_LIST_FROM_TEXT"] = "tạo danh sách từ văn bản";
Blockly.Msg["LISTS_SPLIT_TEXT_FROM_LIST"] = "tạo văn bản từ danh sách";
Blockly.Msg["LISTS_SPLIT_TOOLTIP_JOIN"] = "Liên kết một danh sách các văn bản vào một văn bản, cách nhau bằng dấu phân cách.";
Blockly.Msg["LISTS_SPLIT_TOOLTIP_SPLIT"] = "Tách văn bản thành một danh sách các văn bản nhỏ, ngắt bởi các ký tự phân cách.";
Blockly.Msg["LISTS_SPLIT_WITH_DELIMITER"] = "với ký tự phân cách";
Blockly.Msg["LOGIC_BOOLEAN_FALSE"] = "sai";
Blockly.Msg["LOGIC_BOOLEAN_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#values";  // untranslated
Blockly.Msg["LOGIC_BOOLEAN_TOOLTIP"] = "Hoàn trả \"đúng\" hoặc \"sai\".";
Blockly.Msg["LOGIC_BOOLEAN_TRUE"] = "đúng";
Blockly.Msg["LOGIC_COMPARE_HELPURL"] = "https://vi.wikipedia.org/wiki/B%E1%BA%A5t_%C4%91%E1%BA%B3ng_th%E1%BB%A9c";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_EQ"] = "Hoàn trả giá trị \"đúng\" (true) nếu giá trị hai đầu vào bằng nhau.";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_GT"] = "Hoàn trả giá trị \"đúng\" (true) nếu đầu vào thứ nhất lớn hơn đầu vào thứ hai.";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_GTE"] = "Hoàn trả giá trị \"đúng\" (true) nếu đầu vào thứ nhất lớn hơn hoặc bằng đầu vào thứ hai.";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_LT"] = "Hoàn trả giá trị \"đúng\" (true) nếu đầu vào thứ nhất nhỏ hơn đầu vào thứ hai.";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_LTE"] = "Hoàn trả giá trị \"đúng\" (true) nếu đầu vào thứ nhất nhỏ hơn hoặc bằng đầu vào thứ hai.";
Blockly.Msg["LOGIC_COMPARE_TOOLTIP_NEQ"] = "Hoàn trả giá trị \"đúng\" (true) nếu giá trị hai đầu vào không bằng nhau.";
Blockly.Msg["LOGIC_NEGATE_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#not";  // untranslated
Blockly.Msg["LOGIC_NEGATE_TITLE"] = "không %1";
Blockly.Msg["LOGIC_NEGATE_TOOLTIP"] = "Hoàn trả \"đúng\" (true) nếu đầu vào sai.  Hoàn trả \"sai\" (false) nếu đầu vào đúng.";
Blockly.Msg["LOGIC_NULL"] = "trống không";
Blockly.Msg["LOGIC_NULL_HELPURL"] = "https://en.wikipedia.org/wiki/Nullable_type";  // untranslated
Blockly.Msg["LOGIC_NULL_TOOLTIP"] = "Hoàn trả trống không.";
Blockly.Msg["LOGIC_OPERATION_AND"] = "và";
Blockly.Msg["LOGIC_OPERATION_HELPURL"] = "https://github.com/google/blockly/wiki/Logic#logical-operations";  // untranslated
Blockly.Msg["LOGIC_OPERATION_OR"] = "hoặc";
Blockly.Msg["LOGIC_OPERATION_TOOLTIP_AND"] = "Hoàn trả \"đúng\" (true) nếu cả hai đầu vào đều đúng.";
Blockly.Msg["LOGIC_OPERATION_TOOLTIP_OR"] = "Hoàn trả \"đúng\" (true) nếu ít nhất một trong hai đầu vào đúng.";
Blockly.Msg["LOGIC_TERNARY_CONDITION"] = "kiểm tra";
Blockly.Msg["LOGIC_TERNARY_HELPURL"] = "https://en.wikipedia.org/wiki/%3F:";  // untranslated
Blockly.Msg["LOGIC_TERNARY_IF_FALSE"] = "nếu sai";
Blockly.Msg["LOGIC_TERNARY_IF_TRUE"] = "nếu đúng";
Blockly.Msg["LOGIC_TERNARY_TOOLTIP"] = "Kiểm tra điều kiện. Nếu điều kiện đúng, hoàn trả giá trị từ mệnh đề \"nếu đúng\" nếu không đúng, hoàn trả giá trị từ mệnh đề \"nếu sai\".";
Blockly.Msg["MATH_ADDITION_SYMBOL"] = "+";  // untranslated
Blockly.Msg["MATH_ARITHMETIC_HELPURL"] = "https://vi.wikipedia.org/wiki/S%E1%BB%91_h%E1%BB%8Dc";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_ADD"] = "Hoàn trả tổng của hai con số.";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_DIVIDE"] = "Hoàn trả thương của hai con số.";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_MINUS"] = "Hoàn trả hiệu của hai con số.";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_MULTIPLY"] = "Hoàn trả tích của hai con số.";
Blockly.Msg["MATH_ARITHMETIC_TOOLTIP_POWER"] = "Hoàn trả số lũy thừa với số thứ nhất là cơ số và số thứ hai là số mũ.";
Blockly.Msg["MATH_ATAN2_HELPURL"] = "https://en.wikipedia.org/wiki/Atan2";  // untranslated
Blockly.Msg["MATH_ATAN2_TITLE"] = "atan2 của X:%1 Y:%2";
Blockly.Msg["MATH_ATAN2_TOOLTIP"] = "Trả về arctangent của điểm (X, Y) trong khoảng từ -180 độ đến 180 độ.";
Blockly.Msg["MATH_CHANGE_HELPURL"] = "https://vi.wikipedia.org/wiki/Ph%C3%A9p_c%E1%BB%99ng";
Blockly.Msg["MATH_CHANGE_TITLE"] = "cộng vào %1 giá trị %2";
Blockly.Msg["MATH_CHANGE_TOOLTIP"] = "Cộng số đầu vào vào biến \"%1\".";
Blockly.Msg["MATH_CONSTANT_HELPURL"] = "https://en.wikipedia.org/wiki/Mathematical_constant";  // untranslated
Blockly.Msg["MATH_CONSTANT_TOOLTIP"] = "Hoàn trả các đẳng số thường gặp: π (3.141…), e (2.718…), φ (1.618…), sqrt(2) (1.414…), sqrt(½) (0.707…), or ∞ (vô cực).";
Blockly.Msg["MATH_CONSTRAIN_HELPURL"] = "https://en.wikipedia.org/wiki/Clamping_(graphics)";  // untranslated
Blockly.Msg["MATH_CONSTRAIN_TITLE"] = "giới hạn %1 không dưới %2 không hơn %3";
Blockly.Msg["MATH_CONSTRAIN_TOOLTIP"] = "Giới hạn số đầu vào để không dưới số thứ nhất và không hơn số thứ hai.";
Blockly.Msg["MATH_DIVISION_SYMBOL"] = "÷";  // untranslated
Blockly.Msg["MATH_IS_DIVISIBLE_BY"] = "chia hết cho";
Blockly.Msg["MATH_IS_EVEN"] = "là số chẵn";
Blockly.Msg["MATH_IS_NEGATIVE"] = "là số âm";
Blockly.Msg["MATH_IS_ODD"] = "là số lẻ";
Blockly.Msg["MATH_IS_POSITIVE"] = "là số dương";
Blockly.Msg["MATH_IS_PRIME"] = "là số nguyên tố";
Blockly.Msg["MATH_IS_TOOLTIP"] = "Kiểm tra con số xem nó có phải là số chẵn, lẻ, nguyên tố, nguyên, dương, âm,  hay xem nó có chia hết cho số đầu vào hay không.  Hoàn trả đúng hay sai.";
Blockly.Msg["MATH_IS_WHOLE"] = "là số nguyên";
Blockly.Msg["MATH_MODULO_HELPURL"] = "https://en.wikipedia.org/wiki/Modulo_operation";  // untranslated
Blockly.Msg["MATH_MODULO_TITLE"] = "số dư của %1 ÷ %2";
Blockly.Msg["MATH_MODULO_TOOLTIP"] = "Chia số thứ nhất cho số thứ hai rồi hoàn trả số dư từ.";
Blockly.Msg["MATH_MULTIPLICATION_SYMBOL"] = "×";  // untranslated
Blockly.Msg["MATH_NUMBER_HELPURL"] = "https://vi.wikipedia.org/wiki/S%E1%BB%91";
Blockly.Msg["MATH_NUMBER_TOOLTIP"] = "Một con số.";
Blockly.Msg["MATH_ONLIST_HELPURL"] = "";  // untranslated
Blockly.Msg["MATH_ONLIST_OPERATOR_AVERAGE"] = "giá trị trung bình của một danh sách";
Blockly.Msg["MATH_ONLIST_OPERATOR_MAX"] = "số lớn nhât của một danh sách";
Blockly.Msg["MATH_ONLIST_OPERATOR_MEDIAN"] = "số trung vị của một danh sách";
Blockly.Msg["MATH_ONLIST_OPERATOR_MIN"] = "số nhỏ nhất của một danh sách";
Blockly.Msg["MATH_ONLIST_OPERATOR_MODE"] = "các mode của một danh sách";
Blockly.Msg["MATH_ONLIST_OPERATOR_RANDOM"] = "một số bất kỳ của một danh sách";
Blockly.Msg["MATH_ONLIST_OPERATOR_STD_DEV"] = "độ lệch chuẩn của một danh sách";
Blockly.Msg["MATH_ONLIST_OPERATOR_SUM"] = "tổng của một danh sách";
Blockly.Msg["MATH_ONLIST_TOOLTIP_AVERAGE"] = "Hoàn trả giá trị trung bình từ của danh sách số.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MAX"] = "Hoàn trả số lớn nhất trong tất cả các số trong danh sách.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MEDIAN"] = "Hoàn trả số trung vị của danh sách số.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MIN"] = "Hoàn trả số nhỏ nhất trong tất cả các số trong danh sách.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_MODE"] = "Hoàn trả các số có mặt nhiều nhất trong danh sách.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_RANDOM"] = "Hoàn trả một số bất kỳ từ các số trong danh sách.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_STD_DEV"] = "Hoàn trả độ lệch chuẩn của danh sách số.";
Blockly.Msg["MATH_ONLIST_TOOLTIP_SUM"] = "Hoàn trả tổng số của tất cả các số trong danh sách.";
Blockly.Msg["MATH_POWER_SYMBOL"] = "^";  // untranslated
Blockly.Msg["MATH_RANDOM_FLOAT_HELPURL"] = "https://en.wikipedia.org/wiki/Random_number_generation";  // untranslated
Blockly.Msg["MATH_RANDOM_FLOAT_TITLE_RANDOM"] = "phân số bất kỳ";
Blockly.Msg["MATH_RANDOM_FLOAT_TOOLTIP"] = "Hoàn trả một phân số bất kỳ không nhỏ hơn 0.0 và không lớn hơn 1.0.";
Blockly.Msg["MATH_RANDOM_INT_HELPURL"] = "https://en.wikipedia.org/wiki/Random_number_generation";  // untranslated
Blockly.Msg["MATH_RANDOM_INT_TITLE"] = "Một số nguyên bất kỳ từ %1 đến %2";
Blockly.Msg["MATH_RANDOM_INT_TOOLTIP"] = "Hoàn trả một số nguyên bất kỳ lớn hơn hoặc bằng số đầu và nhỏ hơn hoặc bằng số sau.";
Blockly.Msg["MATH_ROUND_HELPURL"] = "https://en.wikipedia.org/wiki/Rounding";  // untranslated
Blockly.Msg["MATH_ROUND_OPERATOR_ROUND"] = "làm tròn";
Blockly.Msg["MATH_ROUND_OPERATOR_ROUNDDOWN"] = "làm tròn xuống";
Blockly.Msg["MATH_ROUND_OPERATOR_ROUNDUP"] = "làm tròn lên";
Blockly.Msg["MATH_ROUND_TOOLTIP"] = "Làm tròn lên hoặc tròn xuống số đầu vào.";
Blockly.Msg["MATH_SINGLE_HELPURL"] = "https://vi.wikipedia.org/wiki/C%C4%83n_b%E1%BA%ADc_hai";
Blockly.Msg["MATH_SINGLE_OP_ABSOLUTE"] = "giá trị tuyệt đối";
Blockly.Msg["MATH_SINGLE_OP_ROOT"] = "căn bật hai";
Blockly.Msg["MATH_SINGLE_TOOLTIP_ABS"] = "Hoàn trả giá trị tuyệt đối của số đầu vào.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_EXP"] = "Hoàn trả lũy thừa của số e với số mũ đầu vào.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_LN"] = "Hoàn trả lôgarit tự nhiên của số đầu vào.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_LOG10"] = "Hoàn trả lôgarit cơ số 10 của số đầu vào.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_NEG"] = "Đổi dấu của số đầu vào: âm thành dương và dương thành âm, và hoàn trả số mới.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_POW10"] = "Hoàn trả lũy thừa của số 10 với số mũ đầu vào.";
Blockly.Msg["MATH_SINGLE_TOOLTIP_ROOT"] = "Hoàn trả căn bật hai của số đầu vào.";
Blockly.Msg["MATH_SUBTRACTION_SYMBOL"] = "-";  // untranslated
Blockly.Msg["MATH_TRIG_ACOS"] = "acos";
Blockly.Msg["MATH_TRIG_ASIN"] = "asin";
Blockly.Msg["MATH_TRIG_ATAN"] = "atan";
Blockly.Msg["MATH_TRIG_COS"] = "cos";
Blockly.Msg["MATH_TRIG_HELPURL"] = "https://vi.wikipedia.org/wiki/H%C3%A0m_l%C6%B0%E1%BB%A3ng_gi%C3%A1c";
Blockly.Msg["MATH_TRIG_SIN"] = "sin";
Blockly.Msg["MATH_TRIG_TAN"] = "tan";
Blockly.Msg["MATH_TRIG_TOOLTIP_ACOS"] = "Hoàn trả Arccos của một góc (theo độ).";
Blockly.Msg["MATH_TRIG_TOOLTIP_ASIN"] = "Hoàn trả Arcsin của một góc (theo độ).";
Blockly.Msg["MATH_TRIG_TOOLTIP_ATAN"] = "Hoàn trả Arctang của một góc (theo độ).";
Blockly.Msg["MATH_TRIG_TOOLTIP_COS"] = "Hoàn trả Cos của một góc (theo độ).";
Blockly.Msg["MATH_TRIG_TOOLTIP_SIN"] = "Hoàn trả Sin của một góc (theo độ).";
Blockly.Msg["MATH_TRIG_TOOLTIP_TAN"] = "Hoàn trả Tang của một góc (theo độ).";
Blockly.Msg["NEW_COLOUR_VARIABLE"] = "Tạo một giá trị màu sắc...";
Blockly.Msg["NEW_NUMBER_VARIABLE"] = "Tạo một giá trị số...";
Blockly.Msg["NEW_STRING_VARIABLE"] = "Tạo một giá trị dạng chuỗi...";
Blockly.Msg["NEW_VARIABLE"] = "Tạo biến...";
Blockly.Msg["NEW_VARIABLE_TITLE"] = "Tên của biến mới:";
Blockly.Msg["NEW_VARIABLE_TYPE_TITLE"] = "Kiểu giá trị mới:";
Blockly.Msg["ORDINAL_NUMBER_SUFFIX"] = "";  // untranslated
Blockly.Msg["PROCEDURES_ALLOW_STATEMENTS"] = "cho phép báo cáo";
Blockly.Msg["PROCEDURES_BEFORE_PARAMS"] = "với:";
Blockly.Msg["PROCEDURES_CALLNORETURN_HELPURL"] = "https://vi.wikipedia.org/wiki/Ch%C6%B0%C6%A1ng_tr%C3%ACnh_con";
Blockly.Msg["PROCEDURES_CALLNORETURN_TOOLTIP"] = "Chạy một thủ tục không có giá trị hoàn trả.";
Blockly.Msg["PROCEDURES_CALLRETURN_HELPURL"] = "https://vi.wikipedia.org/wiki/Ch%C6%B0%C6%A1ng_tr%C3%ACnh_con";
Blockly.Msg["PROCEDURES_CALLRETURN_TOOLTIP"] = "Chạy một thủ tục có giá trị hoàn trả.";
Blockly.Msg["PROCEDURES_CALL_BEFORE_PARAMS"] = "với:";
Blockly.Msg["PROCEDURES_CREATE_DO"] = "Tạo mảnh \"thực hiện %1\"";
Blockly.Msg["PROCEDURES_DEFNORETURN_COMMENT"] = "Mô tả hàm này...";
Blockly.Msg["PROCEDURES_DEFNORETURN_DO"] = "";  // untranslated
Blockly.Msg["PROCEDURES_DEFNORETURN_HELPURL"] = "https://en.wikipedia.org/wiki/Subroutine";  // untranslated
Blockly.Msg["PROCEDURES_DEFNORETURN_PROCEDURE"] = "làm gì đó";
Blockly.Msg["PROCEDURES_DEFNORETURN_TITLE"] = "thủ tục để";
Blockly.Msg["PROCEDURES_DEFNORETURN_TOOLTIP"] = "Một thủ tục không có giá trị hoàn trả.";
Blockly.Msg["PROCEDURES_DEFRETURN_HELPURL"] = "https://en.wikipedia.org/wiki/Subroutine";  // untranslated
Blockly.Msg["PROCEDURES_DEFRETURN_RETURN"] = "hoàn trả";
Blockly.Msg["PROCEDURES_DEFRETURN_TOOLTIP"] = "Một thủ tục có giá trị hoàn trả.";
Blockly.Msg["PROCEDURES_DEF_DUPLICATE_WARNING"] = "Chú ý: Thủ tục này có lặp lại tên các tham số.";
Blockly.Msg["PROCEDURES_HIGHLIGHT_DEF"] = "Làm nổi bật thủ tục";
Blockly.Msg["PROCEDURES_IFRETURN_HELPURL"] = "http://c2.com/cgi/wiki?GuardClause";  // untranslated
Blockly.Msg["PROCEDURES_IFRETURN_TOOLTIP"] = "Khi điều kiện đúng thì hoàn trả một giá trị.";
Blockly.Msg["PROCEDURES_IFRETURN_WARNING"] = "Chú ý: Mảnh này chỉ có thể dùng trong một thủ tục.";
Blockly.Msg["PROCEDURES_MUTATORARG_TITLE"] = "biến:";
Blockly.Msg["PROCEDURES_MUTATORARG_TOOLTIP"] = "Thêm một đầu vào cho hàm.";
Blockly.Msg["PROCEDURES_MUTATORCONTAINER_TITLE"] = "các tham số";
Blockly.Msg["PROCEDURES_MUTATORCONTAINER_TOOLTIP"] = "Thêm, xóa hoặc sắp xếp lại các đầu vào cho hàm này.";
Blockly.Msg["REDO"] = "Làm lại";
Blockly.Msg["REMOVE_COMMENT"] = "Xóa Chú Giải";
Blockly.Msg["RENAME_VARIABLE"] = "Thay tên biến...";
Blockly.Msg["RENAME_VARIABLE_TITLE"] = "Thay tên tất cả các biến \"%1\" thành:";
Blockly.Msg["TEXT_APPEND_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-modification";  // untranslated
Blockly.Msg["TEXT_APPEND_TITLE"] = "ở cuối %1 thêm văn bản %2";
Blockly.Msg["TEXT_APPEND_TOOLTIP"] = "Thêm một mảng văn bản vào biến \"%1\".";
Blockly.Msg["TEXT_CHANGECASE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#adjusting-text-case";  // untranslated
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_LOWERCASE"] = "thành chữ thường";
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_TITLECASE"] = "thành Chữ In Đầu Mỗi Từ";
Blockly.Msg["TEXT_CHANGECASE_OPERATOR_UPPERCASE"] = "thành CHỮ IN HOA";
Blockly.Msg["TEXT_CHANGECASE_TOOLTIP"] = "Hoàn trả văn bản sau khi chuyển đổi chữ in hoa hay thường.";
Blockly.Msg["TEXT_CHARAT_FIRST"] = "lấy ký tự đầu tiên";
Blockly.Msg["TEXT_CHARAT_FROM_END"] = "lấy từ phía cuối, ký tự thứ";
Blockly.Msg["TEXT_CHARAT_FROM_START"] = "lấy ký tự thứ";
Blockly.Msg["TEXT_CHARAT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#extracting-text";  // untranslated
Blockly.Msg["TEXT_CHARAT_LAST"] = "lấy ký tự cuối cùng";
Blockly.Msg["TEXT_CHARAT_RANDOM"] = "lấy ký tự bất kỳ";
Blockly.Msg["TEXT_CHARAT_TAIL"] = "";  // untranslated
Blockly.Msg["TEXT_CHARAT_TITLE"] = "trong văn bản %1 %2";
Blockly.Msg["TEXT_CHARAT_TOOLTIP"] = "Hoàn trả ký tự ở vị trí đặt ra.";
Blockly.Msg["TEXT_COUNT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#counting-substrings";  // untranslated
Blockly.Msg["TEXT_COUNT_MESSAGE0"] = "đến %1 trong %2";
Blockly.Msg["TEXT_COUNT_TOOLTIP"] = "Đếm số lần một đoạn văn bản xuất hiện trong một đoạn văn bản khác.";
Blockly.Msg["TEXT_CREATE_JOIN_ITEM_TOOLTIP"] = "thêm vật mới vào văn bản.";
Blockly.Msg["TEXT_CREATE_JOIN_TITLE_JOIN"] = "kết nối";
Blockly.Msg["TEXT_CREATE_JOIN_TOOLTIP"] = "Thêm, bỏ, hoặc sắp xếp lại các thành phần để tạo dựng mảnh văn bản này.";
Blockly.Msg["TEXT_GET_SUBSTRING_END_FROM_END"] = "đến từ phía cuối, ký tự thứ";
Blockly.Msg["TEXT_GET_SUBSTRING_END_FROM_START"] = "đến ký tự thứ";
Blockly.Msg["TEXT_GET_SUBSTRING_END_LAST"] = "đến ký tự cuối cùng";
Blockly.Msg["TEXT_GET_SUBSTRING_HELPURL"] = "https://github.com/google/blockly/wiki/Text#extracting-a-region-of-text";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_INPUT_IN_TEXT"] = "trong văn bản";
Blockly.Msg["TEXT_GET_SUBSTRING_START_FIRST"] = "lấy từ ký tự đầu tiên";
Blockly.Msg["TEXT_GET_SUBSTRING_START_FROM_END"] = "lấy từ phía cuối, ký tự thứ";
Blockly.Msg["TEXT_GET_SUBSTRING_START_FROM_START"] = "lấy từ ký tự thứ";
Blockly.Msg["TEXT_GET_SUBSTRING_TAIL"] = "";  // untranslated
Blockly.Msg["TEXT_GET_SUBSTRING_TOOLTIP"] = "Hoàn trả một mảng ký tự ấn định từ trong văn bản.";
Blockly.Msg["TEXT_INDEXOF_HELPURL"] = "https://github.com/google/blockly/wiki/Text#finding-text";  // untranslated
Blockly.Msg["TEXT_INDEXOF_OPERATOR_FIRST"] = "tìm sự có mặt đầu tiên của";
Blockly.Msg["TEXT_INDEXOF_OPERATOR_LAST"] = "tìm sự có mặt cuối cùng của";
Blockly.Msg["TEXT_INDEXOF_TITLE"] = "trong văn bản %1 %2 %3";
Blockly.Msg["TEXT_INDEXOF_TOOLTIP"] = "Hoàn trả vị trí xuất hiện đầu/cuối của văn bản thứ nhất trong văn bản thứ hai.  Nếu không tìm thấy thì hoàn trả số %1.";
Blockly.Msg["TEXT_ISEMPTY_HELPURL"] = "https://github.com/google/blockly/wiki/Text#checking-for-empty-text";  // untranslated
Blockly.Msg["TEXT_ISEMPTY_TITLE"] = "%1 trống không";
Blockly.Msg["TEXT_ISEMPTY_TOOLTIP"] = "Hoàn trả “đúng nếu văn bản không có ký tự nào.";
Blockly.Msg["TEXT_JOIN_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-creation";  // untranslated
Blockly.Msg["TEXT_JOIN_TITLE_CREATEWITH"] = "tạo văn bản từ";
Blockly.Msg["TEXT_JOIN_TOOLTIP"] = "Tạo một văn bản từ các thành phần.";
Blockly.Msg["TEXT_LENGTH_HELPURL"] = "https://github.com/google/blockly/wiki/Text#text-modification";  // untranslated
Blockly.Msg["TEXT_LENGTH_TITLE"] = "độ dài của %1";
Blockly.Msg["TEXT_LENGTH_TOOLTIP"] = "Hoàn trả số lượng ký tự (kể cả khoảng trắng) trong văn bản đầu vào.";
Blockly.Msg["TEXT_PRINT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#printing-text";  // untranslated
Blockly.Msg["TEXT_PRINT_TITLE"] = "in lên màng hình %1";
Blockly.Msg["TEXT_PRINT_TOOLTIP"] = "In ra màng hình một văn bản, con số, hay một giá trị đầu vào khác.";
Blockly.Msg["TEXT_PROMPT_HELPURL"] = "https://github.com/google/blockly/wiki/Text#getting-input-from-the-user";  // untranslated
Blockly.Msg["TEXT_PROMPT_TOOLTIP_NUMBER"] = "Xin người dùng nhập vào một con số.";
Blockly.Msg["TEXT_PROMPT_TOOLTIP_TEXT"] = "Xin người dùng nhập vào một văn bản.";
Blockly.Msg["TEXT_PROMPT_TYPE_NUMBER"] = "Xin người dùng nhập vào con số với dòng hướng dẫn";
Blockly.Msg["TEXT_PROMPT_TYPE_TEXT"] = "Xin người dùng nhập vào văn bản với dòng hướng dẫn";
Blockly.Msg["TEXT_REPLACE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#replacing-substrings";  // untranslated
Blockly.Msg["TEXT_REPLACE_MESSAGE0"] = "thay thế %1 bằng %2 trong %3";
Blockly.Msg["TEXT_REPLACE_TOOLTIP"] = "Thay thế tất cả các lần xuất hiện của văn bản bằng văn bản khác.";
Blockly.Msg["TEXT_REVERSE_HELPURL"] = "https://github.com/google/blockly/wiki/Text#reversing-text";  // untranslated
Blockly.Msg["TEXT_REVERSE_MESSAGE0"] = "đảo ngược %1";
Blockly.Msg["TEXT_REVERSE_TOOLTIP"] = "Đảo ngược thứ tự của các chữ cái trong văn bản.";
Blockly.Msg["TEXT_TEXT_HELPURL"] = "https://en.wikipedia.org/wiki/string_(computer_science)";
Blockly.Msg["TEXT_TEXT_TOOLTIP"] = "Một ký tự, một từ, hay một dòng.";
Blockly.Msg["TEXT_TRIM_HELPURL"] = "https://github.com/google/blockly/wiki/Text#trimming-removing-spaces";  // untranslated
Blockly.Msg["TEXT_TRIM_OPERATOR_BOTH"] = "cắt các không gian từ cả hai mặt của";
Blockly.Msg["TEXT_TRIM_OPERATOR_LEFT"] = "cắt các không gian từ bên trái của";
Blockly.Msg["TEXT_TRIM_OPERATOR_RIGHT"] = "cắt các không gian từ bên phải của";
Blockly.Msg["TEXT_TRIM_TOOLTIP"] = "Hoàn trả bản sao của văn bản sau khi xóa khoảng trắng từ một hoặc hai bên.";
Blockly.Msg["TODAY"] = "Hôm nay";
Blockly.Msg["UNDO"] = "Hoàn tác";
Blockly.Msg["UNNAMED_KEY"] = "không tên";
Blockly.Msg["VARIABLES_DEFAULT_NAME"] = "vật";
Blockly.Msg["VARIABLES_GET_CREATE_SET"] = "Tạo mảnh \"đặt vào %1\"";
Blockly.Msg["VARIABLES_GET_HELPURL"] = "https://github.com/google/blockly/wiki/Variables#get";  // untranslated
Blockly.Msg["VARIABLES_GET_TOOLTIP"] = "Hoàn trả giá trị của.";
Blockly.Msg["VARIABLES_SET"] = "cho %1 bằng %2";
Blockly.Msg["VARIABLES_SET_CREATE_GET"] = "Tạo mảnh \"lấy %1\"";
Blockly.Msg["VARIABLES_SET_HELPURL"] = "https://github.com/google/blockly/wiki/Variables#set";  // untranslated
Blockly.Msg["VARIABLES_SET_TOOLTIP"] = "Đặt giá trị của biến này thành...";
Blockly.Msg["VARIABLE_ALREADY_EXISTS"] = "Một biến có tên '%1' đã tồn tại.";
Blockly.Msg["VARIABLE_ALREADY_EXISTS_FOR_ANOTHER_TYPE"] = "Giá trị '%1' đã tồn tại dưới dạng: '%2'.";
Blockly.Msg["WORKSPACE_ARIA_LABEL"] = "Không gian làm việc Blockly";
Blockly.Msg["WORKSPACE_COMMENT_DEFAULT_TEXT"] = "Hãy nói gì đó...";
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
