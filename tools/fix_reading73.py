"""Round 73: manual reading fixes for 287 confusing strings, inverted terms, and DAW mistranslations.

Major defect classes discovered and fixed in this round:

1. "Dissolve Part" mistranslated as "Hòa tan" (sugar dissolving in water) (3 strings):
   - "Dissolve Part" -> was "Hòa tan Part" -> "Rã Part"
   - "Dissolve Audio Parts" -> was "Hòa tan Audio Part" -> "R�� Audio Part"
   - "Dissolve Note Expression" -> was "Hòa tan Note Expression" -> "Rã Note Expression"

2. Typo "Thiết lật" instead of "Thiết lập" (7 strings):
   - "Project Colors Setup..." -> was "Thiết lật màu Project..." -> "Thiết lập màu Project..."
   - "Project Synchronisation Setup" -> was "Thiết lật đồng bộ Project" -> "Thiết lập đồng bộ Project"
   - "Project Synchronization Setup..." -> was "Thiết lật đồng bộ Project..." -> "Thiết lập đồng bộ Project..."
   - "Set up Lane Controls" -> was "Thiết lật điều khiển Lane" -> "Thiết lập điều khiển Lane"
   - "Set up Sections" -> was "Thiết lật phần" -> "Thiết lập các phần"
   - "Set up Status Line" -> was "Thiết lật thanh trạng thái" -> "Thiết lập Status Line"
   - "Set up Tabs" -> was "Thiết lật thẻ" -> "Thiết lập thẻ"

3. "Stereo Flip" inverted word order (1 string):
   - "Stereo Flip" -> was "Stereo Lật" -> "Đảo kênh Stereo"

4. "Medium" (storage/audio media) mistranslated as "Trung bình" (low/medium/high) (4 strings):
   - "Import Medium" -> was "Import Trung bình" -> "Import Media"
   - "Import Medium..." -> was "Import Trung bình..." -> "Import Media..."
   - "ERROR: Could not link OMF medium!" -> was "LỖI: Không thể liên kết Medium OMF!" -> "LỖI: Không thể liên kết Media OMF!"
   - "Rename Medium" -> was "Đổi tên Medium" -> "Đổi tên Media"

5. "Media Destination Path" & "Reference Media Files" garbled (3 strings):
   - "Media Destination Path" -> was "Media Đích đến Đường dẫn" -> "Đường dẫn đích của Media"
   - "Reference Media Files" -> was "File Reference Media" -> "Các file Media tham chiếu"
   - "Removeable Media" -> was "Media di động" -> "Ổ đĩa di động"

6. "On Import Audio Files" & "Subfolder Next to Exported File" garbled (3 strings):
   - "On Import Audio Files" -> was "File On Import Audio" -> "Khi Import file Audio"
   - "Subfolder Next to Exported File" -> was "Subfolder bên cạnh File Exported" -> "Thư mục con bên cạnh file Export"
   - "On Events" -> was "Bật Event" -> "Event Note-On"

7. "in the project by clicking it" untranslated garbled string (2 strings):
   - "in the project by clicking it" -> was "in the project theo clicking it" -> "trong Project bằng cách nhấp chuột"
   - "in the project via right-click" -> was "Trong Project qua nhấp chuột phải" -> "trong Project bằng cách nhấp chuột phải"

8. "Restore Factory Presets" dropped the verb "Restore" (1 string):
   - "Restore Factory Presets" -> was "Factory Preset" -> "Khôi phục Preset Factory"

9. "Zoom Display Options", "Horizontal Zoom Presets", "Global Meter Settings" inverted (11 strings):
   - "Zoom Display Options" -> was "Zoom Tùy chọn Display" -> "Tùy chọn hiển thị Zoom"
   - "Horizontal Zoom Presets" -> was "Zoom Preset ngang" -> "Preset Zoom ngang"
   - "Organize Zoom Presets" -> was "Sắp xếp Zoom Preset" -> "Sắp xếp Preset Zoom"
   - "Global Meter Settings" -> was "Meter Settings toàn c��c" -> "Cài đặt Meter toàn cục"
   - "Selected Mode Settings" -> was "Mode Settings đã chọn" -> "Cài đặt chế độ đã chọn"
   - "Selected Player Settings" -> was "Player Settings đã chọn" -> "Cài đặt Player đã chọn"
   - "Convert Options" -> was "Chuyển đổi tùy chọn" -> "Tùy chọn chuyển đổi"
   - "Import Options" -> was "Import Tùy chọn" -> "Tùy chọn Import"
   - "Import Setup" -> was "Import Thiết lập" -> "Thiết lập Import"
   - "Randomize Settings" -> was "Ngẫu nhiên hóa cài đặt" -> "Cài đặt ngẫu nhiên hóa"
   - "Switch Presets" -> was "Chuyển sang Preset" -> "Chuyển đổi Preset"

10. "Palette" floating toolbars mistranslated as "bảng màu" (color palette) (2 strings):
    - "Transpose Palette" -> was "Transpose bảng màu" -> "Bảng Transpose"
    - "Zoom Palette" -> was "Bảng màu Zoom" -> "Bảng Zoom"

11. "Zoom 4 Tracks", "Zoom 8 Tracks", "Zoom N Tracks" mistranslated as Track numbers (4 strings):
    - "Zoom 4 Tracks" -> was "Zoom Track 4" -> "Zoom 4 Track"
    - "Zoom 8 Tracks" -> was "Zoom Track 8" -> "Zoom 8 Track"
    - "Zoom N Tracks" -> was "Zoom Track N" -> "Zoom N Track"
    - "Zoom Tracks Exclusive" -> was "Zoom Track độc quyền" -> "Zoom riêng Track đã chọn"

12. "Select Tool" & "Erase Tool" mistranslated as verb phrases (6 strings):
    - "Select Tool" -> was "Chọn công cụ" -> "Công cụ chọn"
    - "Select Tool (Press [ALT] to draw events)" -> was "Chọn công cụ (Nhấn [ALT] để vẽ Event)" -> "Công cụ chọn (Nhấn [ALT] để vẽ Event)"
    - "Select Tool: Show Extra Info" -> was "Chọn công cụ: Hiện thông tin thêm" -> "Công cụ chọn: Hiện thêm thông tin"
    - "Erase Tool" -> was "Xóa công cụ" -> "Công cụ xóa"
    - "Draw Tool" -> was "Công cụ vẽ" -> "Công cụ Draw"
    - "Combine Selection Tools" -> was "Kết hợp công cụ chọn" -> "Kết hợp các công cụ chọn"

13. "Suspended" chords mistranslated as "hợp âm treo cấp..." (10 strings):
    - "Apply suspended fourth chord to selection" -> was "Áp dụng hợp âm treo cấp 4..." -> "Áp dụng hợp âm Sus4 cho vùng chọn"
    - "Apply suspended fourth chord with a 7 to selection" -> was "Áp dụng hợp âm treo 4 với nốt 7..." -> "Áp dụng hợp âm Sus4 với nốt 7 cho vùng chọn"
    - "Apply suspended second chord to selection" -> was "Áp dụng hợp âm treo cấp 2..." -> "Áp dụng hợp âm Sus2 cho vùng chọn"
    - "Apply suspended second chord with a 7 to selection" -> was "Áp dụng hợp âm treo 2 với nốt 7..." -> "Áp dụng hợp âm Sus2 với nốt 7 cho vùng chọn"
    - "Insert a suspended fourth chord" -> was "Chèn hợp âm treo cấp 4" -> "Chèn hợp âm Sus4"
    - "Insert a suspended fourth chord with a 7" -> was "Chèn hợp âm treo 4 với nốt 7" -> "Chèn hợp âm Sus4 với nốt 7"
    - "Insert a suspended second chord" -> was "Chèn hợp âm treo cấp 2" -> "Chèn hợp âm Sus2"
    - "Insert a suspended second chord with a 7" -> was "Chèn hợp âm treo 2 với nốt 7" -> "Chèn hợp âm Sus2 với nốt 7"
    - "Apply diminished 7th chord to selection" -> was "Áp dụng hợp âm giảm cấp 7..." -> "Áp dụng hợp âm 7 giảm cho vùng chọn"
    - "Apply half-diminished 7th chord to selection" -> was "Áp dụng hợp âm nửa giảm cấp 7..." -> "Áp dụng hợp âm 7 nửa giảm cho vùng chọn"

14. Tempo terms, "Tempo out of Range!", "Mượt Tempo", "Visible Tempo Lower/Upper Limit" (26 strings):
    - "Tempo out of Range!" -> was "Tempo out của Range!" -> "Tempo nằm ngoài phạm vi!"
    - "Stretch Tempo Data" -> was "Stretch Tempo Dữ liệu" -> "Kéo giãn dữ liệu Tempo"
    - "Stretch Controller Data" -> was "Dữ liệu Controller co giãn" -> "Kéo giãn dữ liệu Controller"
    - "Scale Tempo Data" -> was "Dữ liệu Scale Tempo" -> "Co giãn dữ liệu Tempo"
    - "Scale Controller Data" -> was "Dữ liệu Scale Controller" -> "Co giãn dữ liệu Controller"
    - "Scale Note Expression Data" -> was "Dữ liệu Scale Note Expression" -> "Co giãn dữ liệu Note Expression"
    - "Scale Automation Data" -> was "Dữ liệu Scale Automation" -> "Co giãn dữ liệu Automation"
    - "Thin Out Data" -> was "Dữ liệu Thin Out" -> "Lược bớt dữ liệu"
    - "Tempo Recording" -> was "Tempo Đang ghi" -> "Ghi Tempo"
    - "Tap Tempo - Display only" -> was "Chỉ Tap Tempo - Display" -> "Tap Tempo - Chỉ hiển thị"
    - "Defined Tempo of Audio File" -> was "Defined Tempo của File Audio" -> "Tempo đã định nghĩa của file Audio"
    - "Tempo Adjustment Functions" -> was "Chức năng Tempo Adjustment" -> "Chức năng điều chỉnh Tempo"
    - "Tempo Detection Panel" -> was "Bảng Tempo Detection" -> "Bảng nhận diện Tempo"
    - "Type of New Tempo Points" -> was "Loại của New Tempo Points" -> "Loại điểm Tempo mới"
    - "New Tempo Points Type" -> was "Loại Tempo Points mới" -> "Loại điểm Tempo mới"
    - "Visible Tempo Lower Limit" -> was "đang hiện Tempo Lower Limit" -> "Giới hạn dưới của Tempo đang hiện"
    - "Visible Tempo Upper Limit" -> was "đang hiện Tempo Upper Limit" -> "Giới hạn trên của Tempo đang hiện"
    - "Visible Loudness Lower Limit" -> was "Giới hạn dưới Loudness đang hiện" -> "Giới hạn dưới của Loudness đang hiện"
    - "Visible Loudness Upper Limit" -> was "Giới hạn trên Loudness đang hiện" -> "Giới hạn trên của Loudness đang hiện"
    - "Tempo in BPM" -> was "Tempo trong BPM" -> "Tempo tính bằng BPM"
    - "Smooth Tempo" -> was "Mượt Tempo" -> "Làm mượt Tempo"
    - "Set Constant Tempo" -> was "Đặt Constant Tempo" -> "Đặt Tempo cố định"
    - "Calculate Tempo from MIDI Events" -> was "Tính Tempo từ MIDI Events" -> "Tính Tempo từ các MIDI Event"
    - "Calculate Tempo from MIDI Events..." -> was "Tính Tempo từ MIDI Events..." -> "Tính Tempo từ các MIDI Event..."
    - "Delete Tempo Events" -> was "Xóa Tempo Events" -> "Xóa các Tempo Event"
    - "Insert Tempo Events" -> was "Chèn Tempo Events" -> "Chèn các Tempo Event"

15. "Project Logical Editor" standardized (5 strings):
    - "Project Logical Editor" -> was "Logical Editor của Project" -> "Project Logical Editor"
    - "Project Logical Editor..." -> was "Logical Editor của Project..." -> "Project Logical Editor..."
    - "Open Project Logical Editor" -> was "Mở Logical Editor của Project" -> "Mở Project Logical Editor"
    - "Open Project Logical Editor..." -> was "Mở Logical Editor của Project..." -> "Mở Project Logical Editor..."
    - "Project Logical Editor Presets" -> was "Preset Logical Editor của Project" -> "Preset Project Logical Editor"

16. 9-Pin RS422 protocol mistranslated as "thiết bị 9 chân" (9 strings):
    - "The 9-Pin device did not recognize the command." -> was "Thiết bị 9 chân không nhận dạng được lệnh." -> "Thiết bị 9-Pin không nhận dạng được lệnh."
    - "SyncStation 9-Pin Device ID" -> was "ID thiết bị SyncStation 9 chân" -> "ID thiết bị 9-Pin của SyncStation"
    - "Time Base 9-Pin Device ID" -> was "ID thiết bị Time Base 9 chân" -> "ID thiết bị 9-Pin của Time Base"
    - "9 Pin Serial Port" -> was "Cổng nối tiếp 9 chân" -> "Cổng nối tiếp 9-Pin"
    - "Use 9 Pin Device 1 as timecode source" -> was "Dùng thiết bị 9 chân 1 làm nguồn Timecode" -> "Dùng thiết bị 9-Pin 1 làm nguồn Timecode"
    - "Use 9 Pin Device 1 for Machine Control" -> was "Dùng thiết bị 9 chân 1 cho Machine Control" -> "Dùng thiết bị 9-Pin 1 cho Machine Control"
    - "Use 9 Pin Device 2 as timecode source" -> was "Dùng thiết bị 9 chân 2 làm nguồn Timecode" -> "Dùng thiết bị 9-Pin 2 làm nguồn Timecode"
    - "Use 9 Pin Device 2 for Machine Control" -> was "Dùng thiết bị 9 chân 2 cho Machine Control" -> "Dùng thiết bị 9-Pin 2 cho Machine Control"
    - "Take position from SyncStation 9Pin port and LTC reader" -> was "Lấy vị trí từ cổng 9 chân SyncStation..." -> "Lấy vị trí t�� cổng 9-Pin của SyncStation và đầu đọc LTC"

17. Focus & Quick Controls consistency (9 strings):
    - "Focus" -> was "Tập trung" -> "Focus"
    - "Focus Quick Controls" -> was "Tập trung Quick Controls" -> "Focus Quick Control"
    - "Quick Control Focus" -> was "Tập trung Quick Control" -> "Quick Control Focus"
    - "Quick Control Focus (Track)" -> was "Tập trung Quick Control (Track)" -> "Quick Control Focus (Track)"
    - "Depth Focus" -> was "Tập trung độ sâu" -> "Depth Focus"
    - "Follow Plug-in Window in Focus" -> was "Theo cửa sổ Plug-in đang được tập trung" -> "Bám theo cửa sổ Plug-in đang Focus"
    - "Plug-in Window Focus Only" -> was "Chỉ tập trung cửa sổ Plug-in" -> "Chỉ Focus cửa sổ Plug-in"
    - "Track Focus Only" -> was "Chỉ tập trung Track" -> "Chỉ Focus Track"
    - "Track and Plug-in Window Focus" -> was "Tập trung cửa sổ Track và Plug-in" -> "Focus cửa sổ Track và Plug-in"

18. "Ruler" and "Time Format" (18 strings):
    - "Time Format" -> was "Thời gian Định dạng" -> "Định dạng thời gian"
    - "Ruler Time Format" -> was "Ruler Thời gian Định dạng" -> "Định dạng thời gian của Ruler"
    - "Ruler Display Format" -> was "Ruler Hiển thị Định dạng" -> "Định dạng hiển thị của Ruler"
    - "Ruler Colors" -> was "Màu thước đo" -> "Màu Ruler"
    - "Ruler Mode: Bars+Beats Linear" -> was "Chế độ thước đo: Bar+Beat tuyến tính" -> "Chế độ Ruler: Bar+Beat tuyến tính"
    - "Ruler Mode: Time Linear" -> was "Chế độ thước đo: thời gian tuyến tính" -> "Chế độ Ruler: Time Linear"
    - "Clicking Locator Range in Upper Part of the Ruler Activates Cycle" -> was "...ở phần trên của thước đo..." -> "Nhấp vào dải Locator ở phần trên của Ruler sẽ bật Cycle"
    - "Select Time Format" -> was "Chọn Time Format" -> "Chọn định dạng thời gian"
    - "Select Prev Time Format" -> was "Chọn Prev Time Format" -> "Chọn định dạng thời gian trước"
    - "Arbitrary Range Start Time in Primary Time Format" -> was "...trong Primary Time Format" -> "Thời gian đầu vùng tùy ý theo Primary Time Format"
    - "Arbitrary Range End Time in Primary Time Format" -> was "...trong Primary Time Format" -> "Thời gian cuối vùng tùy ý theo Primary Time Format"
    - "Range Start Position in Selected Time Format" -> was "...trong Selected Time Format" -> "Vị trí đầu vùng theo định dạng thời gian đã chọn"
    - "Range End Position in Selected Time Format" -> was "...trong Selected Time Format" -> "Vị trí cuối vùng theo định dạng thời gian đã chọn"
    - "New Range End Position in Selected Time Format" -> was "...trong Selected Time Format" -> "Vị trí cuối vùng mới theo định dạng thời gian đã chọn"
    - "New Range Length in Selected Time Format" -> was "...trong Selected Time Format" -> "Độ dài vùng mới theo định dạng thời gian đã chọn"
    - "Range in Primary Time Format" -> was "Vùng trong Primary Time Format" -> "Vùng theo Primary Time Format"

19. "Info Line" and "Status Line" consistency (6 strings):
    - "Info Line" -> was "Dòng thông tin" -> "Info Line"
    - "Set up Info Line" -> was "Thiết lập dòng thông tin" -> "Thiết lập Info Line"
    - "Show Info Line" -> was "Hiện dòng thông tin" -> "Hiện Info Line"
    - "Status Line" -> was "Thanh trạng thái" -> "Status Line"
    - "Show/Hide Status Line" -> was "Hiện/Ẩn thanh trạng thái" -> "Hiện/Ẩn Status Line"
    - "Overview Line" -> was "Dòng tổng quan" -> "Overview Line"

20. Tautologies & double names ("Skins", "Theme", "This Computer", "Doesn't seem to be a valid skin file!") (4 strings):
    - "Skins" -> was "Giao diện Skin" -> "Skin"
    - "Theme" -> was "Giao diện Theme" -> "Theme"
    - "This Computer" -> was "Computer này" -> "Máy tính này"
    - "Doesn't seem to be a valid skin file!" -> was "Có vẻ không phải là file giao diện (Skin) hợp lệ!" -> "Đây có vẻ không phải là file Skin hợp lệ!"

21. Queue, Job, Pool & Link Group fixes (18 strings):
    - "Export Queue" -> was "Export Queue" -> "Hàng đợi Export"
    - "Add Job to Queue" -> was "Thêm Job vào Queue" -> "Thêm tác vụ vào hàng đợi"
    - "Start Queue Export" -> was "Bắt đầu Queue Export" -> "Bắt đầu Export hàng đợi"
    - "Remove Job" -> was "Gỡ bỏ Job" -> "Gỡ bỏ tác vụ"
    - "Update Job" -> was "Cập nhật Job" -> "Cập nhật tác vụ"
    - "To save your changes for the selected job, please click 'Update Job'." -> "...vui lòng nhấp 'Cập nhật tác vụ'."
    - "Find Selected in Pool" -> was "Tìm đã chọn trong Pool" -> "Tìm mục đã chọn trong Pool"
    - "Set Pool Record Folder" -> was "Đặt Pool Record Folder" -> "Đặt thư mục ghi âm của Pool"
    - "Pool Record Folder" -> was "Thư mục Pool Record" -> "Thư mục ghi âm của Pool"
    - "Pool Record Folder:" -> was "Thư mục ghi Pool:" -> "Thư mục ghi âm của Pool:"
    - "Remove Channel from Link Group \"%s\"" -> was "Gỡ bỏ Channel từ Liên kết Gộp nhóm \"%s\"" -> "Gỡ bỏ Channel khỏi Link Group \"%s\""
    - "Remove VCA Channel from Link Group \"%s\"" -> was "Gỡ bỏ VCA Channel từ Liên kết Gộp nhóm \"%s\"" -> "Gỡ bỏ VCA Channel khỏi Link Group \"%s\""
    - "Link Group" -> was "Liên kết Group" -> "Link Group"
    - "Unlink Channels" -> was "Hủy liên kết Channels" -> "Hủy liên kết các Channel"
    - "Unlink Selected Channels" -> was "Hủy liên kết Channels đã chọn" -> "Hủy liên kết các Channel đã chọn"
    - "Add Selected as MMC Slaves" -> was "Thêm đã chọn như MMC Slaves" -> "Thêm các mục đã chọn làm MMC Slave"
    - "Add Selected as Remote Slaves" -> was "Thêm đã chọn như Remote Slaves" -> "Thêm các mục đã chọn làm Remote Slave"
    - "Import video events as marker?" -> was "Import video events như marker?" -> "Import các Video Event làm Marker?"

22. Natural polite Vietnamese error handling ("thất bại" -> "không thành công" / "không thể") (13 strings):
    - "Auto Save failed, because the project is corrupt..." -> "Không thể tự động lưu vì Project bị hỏng..."
    - "Conversion failed!" -> "Chuyển đổi không thành công!"
    - "Data Transfer failed..." -> "Không thể chuyển dữ liệu..."
    - "Database creation failed because the target is write protected..." -> "Không thể tạo cơ sở dữ liệu vì đích bị bảo vệ ghi..."
    - "Database removal failed because the data could not be transferred." -> "Không thể xóa cơ sở dữ liệu vì không truyền được dữ liệu."
    - "Database removal failed because the database file is write protected..." -> "Không thể xóa cơ sở dữ liệu vì file cơ sở dữ liệu bị bảo vệ ghi..."
    - "Processing Failed" -> "Xử lý không thành công"
    - "Reactivating the plug-in failed..." -> "Không thể kích hoạt lại Plug-in!..."
    - "The quick loudness analysis failed. An internal error occurred." -> "Phân tích Loudness nhanh không thành công. Đã xảy ra lỗi nội bộ."
    - "Unpack Project Failed!" -> "Không thể giải nén Project!"
    - "Verify failed for this node!" -> "Xác minh không thành công cho node này!"
    - "Skin parsing failed" -> "Phân tích file Skin không thành công"

23. Miscellaneous UI, Notation, and Audio consistency (60+ strings):
    - "Click during Count-In" -> was "Nhấp trong lúc Count-In" -> "Click trong lúc Count-In"
    - "Start Preview Mode" -> was "Chế độ Preview bắt đầu" -> "Bắt đầu chế độ Preview"
    - "Set Preview Start to Cursor" -> was "Đặt Preview Start tới Cursor" -> "Đặt điểm bắt đầu Preview tại Cursor"
    - "Fill View[Score View Option]" -> was "Lấp đầy chế độ xem" -> "Chế độ xem: Fill View"
    - "Start Time" -> was "Thời gian Start" -> "Thời gian bắt đầu"
    - "Start Position" -> was "Vị trí Start" -> "Vị trí bắt đầu"
    - "Show/Hide Direct Routing" -> was "Hiện/Ẩn Routing trực tiếp" -> "Hiện/Ẩn Direct Routing"
    - "Show Routing as <%s>" -> was "Hiện Routing như <%s>" -> "Hiện Routing dạng <%s>"
    - "Are you sure you want to deactivate all cue sends?" -> was "Bạn có chắc muốn Tắt tất cả cue sends không?" -> "Bạn có chắc muốn tắt tất cả Cue Send không?"
    - "Activate Cue Sends" -> was "Bật Cue Sends" -> "Bật Cue Send"
    - "Deactivate Cue Sends" -> was "Tắt Cue Sends" -> "Tắt Cue Send"
    - "Reset All Cue Sends" -> was "Đặt lại tất cả Cue Sends" -> "Đặt lại tất cả Cue Send"
    - "Open Modulators in Window" -> was "Mở Modulators trong Window" -> "Mở các Modulator trong Window"
    - "Show Modulators in Lower Zone" -> was "Hiện Modulators trong Lower Zone" -> "Hiện các Modulator trong Lower Zone"
    - "Export list as text" -> was "Export list dưới dạng text" -> "Export danh sách dưới dạng văn bản"
    - "Export Key Command Assignments" -> was "Export gán phím tắt" -> "Export phím tắt đã gán"
    - "Key Command Assignments..." -> was "Gán phím tắt..." -> "Các phím tắt đã gán..."
    - "Initial assignment of input movements to VST Note Expressions" -> was "Phân gán ban đầu các chuyển động đầu vào..." -> "Gán ban đầu các thao tác đầu vào cho VST Note Expression"
    - "Replace Audio in Project" -> was "Replace Audio trong Project" -> "Thay thế Audio trong Project"
    - "Replace Audio in Video" -> was "Replace Audio trong Video" -> "Thay thế Audio trong Video"
    - "Replace Audio in Video File..." -> was "Replace Audio trong File Video..." -> "Thay thế Audio trong file Video..."
    - "New + Replace in Pool" -> was "New + Replace trong Pool" -> "Mới + Thay thế trong Pool"
    - "Replacement of PFX" -> was "Replacement của PFX" -> "Thay thế PFX"
    - "Set Transparency for Comparison Channel Curve" -> was "Đặt Transparency cho Comparison Channel Curve" -> "Đặt độ trong suốt cho đường cong Channel so sánh"
    - "Transparency for Comparison Channel Curve:" -> was "Transparency cho Comparison Channel Curve:" -> "Độ trong suốt cho đường cong Channel so sánh:"
    - "EQ Comparison Channel" -> was "EQ Comparison Channel" -> "Channel so sánh EQ"
    - "No Comparison Channel" -> was "Không có Comparison Channel" -> "Không có Channel so sánh"
    - "Send Destination, Gain & Send Controls" -> was "Destination, Gain & Điều khiển Send" -> "Đích Send, Gain & Điều khiển Send"
    - "Select MIDI Send Destination" -> was "Chọn MIDI Send Destination" -> "Chọn đích của MIDI Send"
    - "Send Destination & Gain (Compact)" -> was "Đích & Gain Send (Gọn)" -> "Đích Send & Gain (Gọn)"
    - "Import Master Track" -> was "Import Track Master" -> "Import Master Track"
    - "Project Templates" -> was "Mẫu của Project" -> "Project Template"
    - "Without Channel Settings (Transfer All Settings from Source to New Track)" -> was "Không có cài đặt Channel..." -> "Không kèm cài đặt Channel (Chuyển tất cả cài đặt từ nguồn sang Track mới)"
    - "Render Audio Click between Locators" -> was "Render Audio Click giữa Locators" -> "Render Audio Click giữa hai Locator"
    - "Render MIDI Click between Locators" -> was "Render MIDI Click giữa Locators" -> "Render MIDI Click giữa hai Locator"
    - "New Audio Drivers Found" -> was "Đã tìm thấy trình điều khiển Audio mới" -> "Tìm thấy Driver Audio mới"
    - "New Sample Rate" -> was "Tạo Sample Rate" -> "Sample Rate mới"
    - "HW Sample Rate" -> was "Tỉ lệ HW Sample" -> "Sample Rate phần cứng"
    - "New MIDI Loop" -> was "Tạo MIDI Loop" -> "MIDI Loop mới"
    - "New VCA Channel" -> was "Tạo VCA Channel" -> "VCA Channel mới"
    - "Deactivate all third party plug-ins" -> was "Tắt tất cả third party plug-ins" -> "Tắt tất cả Plug-in bên thứ ba"
    - "External Plug-ins" -> was "External Plug-ins" -> "Các Plug-in ngoài"
    - "Save Plug-in Report" -> was "Lưu Plug-in Report" -> "Lưu báo cáo Plug-in"
    - "Open Plug-in Manager" -> was "Mở trình quản lý Plug-in" -> "Mở Plug-in Manager"
    - "Show/Hide Plug-ins" -> was "Hiện/Ẩn Plug-ins" -> "Hiện/Ẩn Plug-in"
    - "Show/Hide VST Plug-in Pictures" -> was "Hiện/Ẩn VST Plug-in Pictures" -> "Hiện/Ẩn hình ảnh VST Plug-in"
    - "Routing with Plug-in Picture" -> was "Routing với Plug-in Picture" -> "Routing kèm hình ảnh Plug-in"
    - "Add VST Plug-in Picture to Media Rack" -> was "Thêm VST Plug-in Picture vào Media Rack" -> "Thêm hình ảnh VST Plug-in vào Media Rack"
    - "Apply MIDI Velocity Variance" -> was "Áp dụng phân tán Velocity MIDI" -> "Áp dụng độ biến thiên Velocity MIDI"
    - "Reset MIDI Velocity Variance" -> was "Đặt lại phân tán Velocity MIDI" -> "Đặt lại độ biến thiên Velocity MIDI"
    - "Set Velocity Variance" -> was "Đặt phân tán Velocity" -> "Đặt độ biến thiên Velocity"
    - "Punch Points" -> was "Điểm Punch" -> "Punch Point"
    - "Show/Hide Chord Pads" -> was "Hiện/Ẩn Chord Pads" -> "Hiện/Ẩn Chord Pad"
    - "Insert Selected In Arranger Chain" -> was "Chèn đã chọn trong Arranger Chain" -> "Chèn mục đã chọn vào Arranger Chain"
    - "Rename Arranger Events" -> was "Đổi tên Arranger Events" -> "Đổi tên Arranger Event"
    - "Extract Markers from Wave File" -> was "Trích xuất Markers từ Wave File" -> "Trích xuất Marker từ file Wave"
    - "Extract Sound from Track Preset" -> was "Trích xuất Sound từ Preset Track" -> "Trích xuất Sound từ Track Preset"
    - "Project Preview start set to project cursor position." -> was "Điểm bắt đầu xem trước Project được đặt theo vị trí con trỏ Project." -> "Điểm bắt đầu của Project Preview được đặt tại vị trí con trỏ Project."
    - "It is not possible to create a shared copy... A real copy was created instead." -> was "...Một bản sao thực tế đã được tạo thay thế." -> "Không thể tạo bản sao chia sẻ nếu Timebase của các Track không khớp.\\nMột bản sao độc lập đã được tạo để thay thế."
    - "An exception occurred. Save your work and restart the application.\\nThe exception was thrown because of the plug-in :\\n\\n" -> "Đã xảy ra lỗi ngoại lệ. Hãy lưu công việc của bạn và khởi động lại ứng dụng.\\nLỗi phát sinh do Plug-in :\\n\\n"
    - "Follow Beat Grouping" -> "Bám theo cách gom nhóm phách"
    - "Note Grouping" -> "Gom nhóm Note"
    - "All Multi-Channel Tracks" -> "Tất cả các Track đa kênh"
    - "Split Multi-Channel Tracks" -> "Tách các Multi-Channel Track"
    - "Import Position for New Tracks" -> "Vị trí Import cho các Track mới"
    - "Import Controller as Automation Tracks" -> "Import Controller làm Automation Track"
    - "Import Track Picture" -> "Import hình ảnh Track"
    - "Import Position" -> "Vị trí Import"
    - "Import Karaoke Lyrics as Text" -> "Import lời Karaoke dưới dạng văn bản"
    - "Import Key Switches from Instrument" -> "Import Key Switch từ Instrument"
    - "Markers Window" -> "Cửa sổ Marker"
    - "Open Markers Window" -> "Mở cửa sổ Marker"
    - "Insert Chord Notes" -> "Chèn các nốt hợp âm"
    - "VCA Settings Options" -> "Tùy chọn cài đặt VCA"
    - "Send machine control commads to selected SyncStation port" -> "Gửi lệnh Machine Control tới cổng SyncStation đã chọn"
    - "Set Channel Type Filter\\nUse [CTRL + click] to Reset Channel Type Filter" -> "Thiết lập bộ lọc loại Channel\\nDùng [CTRL + nhấp chuột] để đặt lại bộ lọc loại Channel"
    - "Set Channel Visibility Agents\\nUse [ALT]-Click to Reset Channel Visibility Agents" -> "Thiết lập Channel Visibility Agent\\nDùng [ALT] + nhấp chuột để đặt lại Channel Visibility Agent"
    - "Edit Pitch" -> "Sửa Pitch"
    - "Set Pitch" -> "Đặt Pitch"
    - "Highest Pitch" -> "Pitch cao nhất"
    - "Lowest Pitch" -> "Pitch thấp nhất"
    - "Original Pitch" -> "Pitch gốc"
    - "Original Segment Pitch" -> "Pitch gốc của Segment"
    - "Separate Pitches" -> "Tách riêng các Pitch"
    - "Quantize Pitches to Scale" -> "Quantize Pitch theo Scale"
    - "Show Pitches with Events" -> "Hiện Pitch có Event"
    - "Sort Lanes by Pitch" -> "Sắp xếp Lane theo Pitch"
    - "Transposed Pitch" -> "Pitch đã Transpose"
    - "Vertical Pitch Spread" -> "Độ phân bố Pitch theo chiều dọc"
    - "Create Groove Quantize Preset from Hitpoints" -> "Tạo Preset Groove Quantize từ Hitpoint"
    - "Notes Starting on a Beat Followed by a Rest in the Middle of the Beat" -> "Các nốt bắt đầu tại phách và theo sau là dấu lặng ở giữa phách"
    - "Notes Starting on a Beat Ending in the Middle of the Beat" -> "Các nốt bắt đầu tại phách và kết thúc ở giữa phách"
    - "Cross Staff: Cross to Staff Above" -> "Chuyển khuông: Đưa lên khuông nhạc trên"
    - "Cross Staff: Cross to Staff Below" -> "Chuyển khuông: Đưa xuống khuông nhạc dưới"
    - "Cross Staff: Move to Staff Above" -> "Chuyển khuông: Di chuyển lên khuông trên"
    - "Cross Staff: Move to Staff Below" -> "Chuyển khuông: Di chuyển xuống khuông dưới"
    - "Cross Staff: Reset to Original Staff" -> "Chuyển khuông: Đặt lại về khuông gốc"
    - "Show Normal Bar Number If Coincident with Start of Multi-Bar Rest Showing Range" -> "Hiện số Bar thông thường nếu trùng với đầu dải dấu lặng nhiều Bar"
    - "Show Ranges of Bar Numbers Under Multi-Bar Rests and Consolidated Bar Repeats" -> "Hiện dải số Bar dưới dấu lặng nhiều Bar và ký hiệu lặp Bar gộp"
    - "Default Warping Algorithm" -> "Thuật toán Warping mặc định"
    - "Warping Algorithm for Audio Clip" -> "Thuật toán Warping cho Audio Clip"
    - "Open Direct Offline Processing Window" -> "Mở cửa sổ Direct Offline Processing"
    - "Open Sampler Control Window" -> "Mở cửa sổ Sampler Control"
    - "Open Naming Scheme Window" -> "Mở cửa sổ Naming Scheme"
    - "Naming Scheme - Channel Batch Arranger Chain" -> "Quy tắc đặt tên - Channel Batch Arranger Chain"
    - "Naming Scheme - Single Channel Arranger Chain" -> "Quy tắc đặt tên - Single Channel Arranger Chain"
    - "Set Audio Signature" -> "Đặt số chỉ nhịp của Audio"
    - "Paste Click Pattern to Selected Signatures" -> "Dán Click Pattern vào các số chỉ nhịp đã chọn"
    - "Remote Trigger Mode: Use either key switches or program changes to switch between Sound Slots" -> "Chế độ kích hoạt Remote: Dùng Key Switch hoặc Program Change để chuyển đổi giữa các Sound Slot"
    - "Expression Maps" -> "Các Expression Map"
    - "Expression Map: Articulations" -> "Expression Map: Articulation"
    - "Import MIDI Devices" -> "Import các MIDI Device"
    - "Export MIDI Device Setup" -> "Export thiết lập MIDI Device"
    - "Import MIDI Device Setup" -> "Import thiết lập MIDI Device"
    - "Exporting Track Nr: %d ..." -> "Đang Export Track số: %d..."
    - "Import audio tracks from video" -> "Import Audio Track từ Video"
    - "VST 2 Plug-in Path Settings" -> "Cài đặt đường dẫn VST 2 Plug-in"
    - "Reset FFT Post EQ Peak Hold Curve" -> "Đặt lại đường cong giữ đỉnh FFT Post EQ"
    - "Delay in ms" -> "Delay tính bằng ms"
    - "Delay" -> "Delay"
    - "Audio in musical mode cannot be sliced.\\nDo you want to disable musical mode?" -> "Audio ở chế độ Musical không thể cắt thành Slice.\\nBạn có muốn tắt chế độ Musical không?"
    - "Sliced audio cannot be switched to musical mode." -> "Audio đã tạo Slice không thể chuyển sang chế độ Musical."
    - "'%s' is not supported for clips in musical mode!" -> "'%s' không được hỗ trợ cho Clip ở chế độ Musical!"

Usage:
  python tools/fix_reading73.py
  python tools/fix_reading73.py --write
"""
import json, re, os, glob, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BATCH_DIR = os.path.join(ROOT, 'translations', 'batches')
WRITE = '--write' in sys.argv

src = {}
for line in open(os.path.join(ROOT, 'keys', 'all_strings.tsv'),
                 encoding='utf-8').read().splitlines()[1:]:
    if '\t' in line:
        k, u = line.split('\t', 1)
        src[k] = u
vi = json.load(open(os.path.join(ROOT, 'translations', 'vi.json'),
                    encoding='utf-8'))
PH = re.compile(r'%(?:(?:\.\d+)?[a-zA-Z%]|l)')

WORDING = {
    # 1. Dissolve
    'Dissolve Part':
        'Rã Part',
    'Dissolve Audio Parts':
        'Rã Audio Part',
    'Dissolve Note Expression':
        'Rã Note Expression',

    # 2. Typos of Thiết lập
    'Project Colors Setup...':
        'Thiết lập màu Project...',
    'Project Synchronisation Setup':
        'Thiết lập đồng bộ Project',
    'Project Synchronization Setup...':
        'Thiết lập đồng bộ Project...',
    'Set up Lane Controls':
        'Thiết lập điều khiển Lane',
    'Set up Sections':
        'Thiết lập các phần',
    'Set up Status Line':
        'Thiết lập Status Line',
    'Set up Tabs':
        'Thiết lập thẻ',

    # 3. Stereo Flip
    'Stereo Flip':
        'Đảo kênh Stereo',

    # 4. Medium
    'Import Medium':
        'Import Media',
    'Import Medium...':
        'Import Media...',
    'ERROR: Could not link OMF medium!':
        'LỖI: Không thể liên kết Media OMF!',
    'Rename Medium':
        'Đổi tên Media',

    # 5. Media Path / Reference Media Files
    'Media Destination Path':
        'Đường dẫn đích của Media',
    'Reference Media Files':
        'Các file Media tham chiếu',
    'Removeable Media':
        'Ổ đĩa di động',

    # 6. On Import & Subfolder & On Events
    'On Import Audio Files':
        'Khi Import file Audio',
    'Subfolder Next to Exported File':
        'Thư mục con bên cạnh file Export',
    'On Events':
        'Event Note-On',

    # 7. in the project by clicking it
    'in the project by clicking it':
        'trong Project bằng cách nhấp chuột',
    'in the project via right-click':
        'trong Project bằng cách nhấp chuột phải',

    # 8. Restore Factory Presets
    'Restore Factory Presets':
        'Khôi phục Preset Factory',

    # 9. Inverted Zoom / Settings / Options
    'Zoom Display Options':
        'Tùy chọn hiển thị Zoom',
    'Horizontal Zoom Presets':
        'Preset Zoom ngang',
    'Organize Zoom Presets':
        'Sắp xếp Preset Zoom',
    'Global Meter Settings':
        'Cài đặt Meter toàn cục',
    'Selected Mode Settings':
        'Cài đặt chế độ đã chọn',
    'Selected Player Settings':
        'Cài đặt Player đã chọn',
    'Convert Options':
        'Tùy chọn chuyển đổi',
    'Import Options':
        'Tùy chọn Import',
    'Import Setup':
        'Thiết lập Import',
    'Randomize Settings':
        'Cài đặt ngẫu nhiên hóa',
    'Switch Presets':
        'Chuyển đổi Preset',

    # 10. Palettes
    'Transpose Palette':
        'Bảng Transpose',
    'Zoom Palette':
        'Bảng Zoom',

    # 11. Zoom N Tracks
    'Zoom 4 Tracks':
        'Zoom 4 Track',
    'Zoom 8 Tracks':
        'Zoom 8 Track',
    'Zoom N Tracks':
        'Zoom N Track',
    'Zoom Tracks Exclusive':
        'Zoom riêng Track đã chọn',

    # 12. Tools
    'Select Tool':
        'Công cụ chọn',
    'Select Tool (Press [ALT] to draw events)':
        'Công cụ chọn (Nhấn [ALT] để vẽ Event)',
    'Select Tool: Show Extra Info':
        'Công cụ chọn: Hiện thêm thông tin',
    'Erase Tool':
        'Công cụ xóa',
    'Draw Tool':
        'Công cụ Draw',
    'Combine Selection Tools':
        'Kết hợp các công cụ chọn',

    # 13. Chords
    'Apply suspended fourth chord to selection':
        'Áp dụng hợp âm Sus4 cho vùng chọn',
    'Apply suspended fourth chord with a 7 to selection':
        'Áp dụng hợp âm Sus4 với nốt 7 cho vùng chọn',
    'Apply suspended second chord to selection':
        'Áp dụng hợp âm Sus2 cho vùng chọn',
    'Apply suspended second chord with a 7 to selection':
        'Áp dụng hợp âm Sus2 với nốt 7 cho vùng chọn',
    'Insert a suspended fourth chord':
        'Chèn hợp âm Sus4',
    'Insert a suspended fourth chord with a 7':
        'Chèn hợp âm Sus4 với nốt 7',
    'Insert a suspended second chord':
        'Chèn hợp âm Sus2',
    'Insert a suspended second chord with a 7':
        'Chèn hợp âm Sus2 với nốt 7',
    'Apply diminished 7th chord to selection':
        'Áp dụng hợp âm 7 giảm cho vùng chọn',
    'Apply half-diminished 7th chord to selection':
        'Áp dụng hợp âm 7 nửa giảm cho vùng chọn',

    # 14. Tempo
    'Tempo out of Range!':
        'Tempo nằm ngoài phạm vi!',
    'Stretch Tempo Data':
        'Kéo giãn dữ liệu Tempo',
    'Stretch Controller Data':
        'Kéo giãn dữ liệu Controller',
    'Scale Tempo Data':
        'Co giãn dữ liệu Tempo',
    'Scale Controller Data':
        'Co giãn dữ liệu Controller',
    'Scale Note Expression Data':
        'Co giãn dữ liệu Note Expression',
    'Scale Automation Data':
        'Co giãn dữ liệu Automation',
    'Thin Out Data':
        'Lược bớt dữ liệu',
    'Tempo Recording':
        'Ghi Tempo',
    'Tap Tempo - Display only':
        'Tap Tempo - Chỉ hiển thị',
    'Defined Tempo of Audio File':
        'Tempo đã định nghĩa của file Audio',
    'Tempo Adjustment Functions':
        'Chức năng điều chỉnh Tempo',
    'Tempo Detection Panel':
        'Bảng nhận diện Tempo',
    'Type of New Tempo Points':
        'Loại điểm Tempo mới',
    'New Tempo Points Type':
        'Loại điểm Tempo mới',
    'Visible Tempo Lower Limit':
        'Giới hạn dưới của Tempo đang hiện',
    'Visible Tempo Upper Limit':
        'Giới hạn trên của Tempo đang hiện',
    'Visible Loudness Lower Limit':
        'Giới hạn dưới của Loudness đang hiện',
    'Visible Loudness Upper Limit':
        'Giới hạn trên của Loudness đang hiện',
    'Tempo in BPM':
        'Tempo tính bằng BPM',
    'Smooth Tempo':
        'Làm mượt Tempo',
    'Set Constant Tempo':
        'Đặt Tempo cố định',
    'Calculate Tempo from MIDI Events':
        'Tính Tempo từ các MIDI Event',
    'Calculate Tempo from MIDI Events...':
        'Tính Tempo từ các MIDI Event...',
    'Delete Tempo Events':
        'Xóa các Tempo Event',
    'Insert Tempo Events':
        'Chèn các Tempo Event',
    'Multiple tempos were detected in the selected event. \\nApply the Smooth Tempo function if the tempo of the material is assumed to be constant.':
        'Phát hiện nhiều Tempo trong Event đã chọn. \\nÁp dụng chức năng Smooth Tempo nếu Tempo của chất liệu là cố định.',
    'Tempo events are generated up to the point, where an irregular tempo change is detected.\\nApply the Smooth Tempo function if the tempo of the material is assumed to be constant.':
        'Các Tempo Event được tạo tới điểm phát hiện thay đổi Tempo bất thường.\\nÁp dụng chức năng Smooth Tempo nếu Tempo của chất liệu là cố định.',
    # 15. Project Logical Editor
    'Project Logical Editor':
        'Project Logical Editor',
    'Project Logical Editor...':
        'Project Logical Editor...',
    'Open Project Logical Editor':
        'Mở Project Logical Editor',
    'Open Project Logical Editor...':
        'Mở Project Logical Editor...',
    'Project Logical Editor Presets':
        'Preset Project Logical Editor',

    # 16. 9-Pin Devices
    'The 9-Pin device did not recognize the command.':
        'Thiết bị 9-Pin không nhận dạng được lệnh.',
    'SyncStation 9-Pin Device ID':
        'ID thiết bị 9-Pin của SyncStation',
    'Time Base 9-Pin Device ID':
        'ID thiết bị 9-Pin của Time Base',
    '9 Pin Serial Port':
        'Cổng nối tiếp 9-Pin',
    'Use 9 Pin Device 1 as timecode source':
        'Dùng thiết bị 9-Pin 1 làm nguồn Timecode',
    'Use 9 Pin Device 1 for Machine Control':
        'Dùng thiết bị 9-Pin 1 cho Machine Control',
    'Use 9 Pin Device 2 as timecode source':
        'Dùng thiết bị 9-Pin 2 làm nguồn Timecode',
    'Use 9 Pin Device 2 for Machine Control':
        'Dùng thiết bị 9-Pin 2 cho Machine Control',
    'Take position from SyncStation 9Pin port and LTC reader':
        'Lấy vị trí từ cổng 9-Pin của SyncStation và đầu đọc LTC',

    # 17. Focus & Quick Controls
    'Focus':
        'Focus',
    'Focus Quick Controls':
        'Focus Quick Control',
    'Quick Control Focus':
        'Quick Control Focus',
    'Quick Control Focus (Track)':
        'Quick Control Focus (Track)',
    'Depth Focus':
        'Depth Focus',
    'Follow Plug-in Window in Focus':
        'Bám theo cửa sổ Plug-in đang Focus',
    'Plug-in Window Focus Only':
        'Chỉ Focus cửa sổ Plug-in',
    'Track Focus Only':
        'Chỉ Focus Track',
    'Track and Plug-in Window Focus':
        'Focus cửa sổ Track và Plug-in',

    # 18. Ruler & Time Format
    'Time Format':
        'Định dạng thời gian',
    'Ruler Time Format':
        'Định dạng thời gian của Ruler',
    'Ruler Display Format':
        'Định dạng hiển thị của Ruler',
    'Ruler Colors':
        'Màu Ruler',
    'Ruler Mode: Bars+Beats Linear':
        'Chế độ Ruler: Bar+Beat tuyến tính',
    'Ruler Mode: Time Linear':
        'Chế độ Ruler: Time Linear',
    'Clicking Locator Range in Upper Part of the Ruler Activates Cycle':
        'Nhấp vào dải Locator ở phần trên của Ruler sẽ bật Cycle',
    "Ruler Display Type has been changed to \\'Bar + Beats\\'.  This is required for Metronome Click Pattern Emphasis.":
        "Kiểu hiển thị của Ruler đã đổi thành 'Bar + Beats'.  Điều này là bắt buộc để làm nổi bật Pattern Click Metronome.",
    "Ruler Display Type has been changed to \\'Bar + Beats\\' and the Grid Type to \\'Use Quantize\\'.  This is required for Metronome Click Pattern Emphasis.":
        "Kiểu hiển thị của Ruler đã đổi thành 'Bar + Beats' và loại Grid thành 'Dùng Quantize'. Điều này là bắt buộc để làm nổi bật Pattern Click Metronome.",
    'Select Time Format':
        'Chọn định dạng thời gian',
    'Select Prev Time Format':
        'Chọn định dạng thời gian trước',
    'Arbitrary Range Start Time in Primary Time Format':
        'Thời gian đầu vùng tùy ý theo Primary Time Format',
    'Arbitrary Range End Time in Primary Time Format':
        'Thời gian cuối vùng tùy ý theo Primary Time Format',
    'Range Start Position in Selected Time Format':
        'Vị trí đầu vùng theo định dạng thời gian đã chọn',
    'Range End Position in Selected Time Format':
        'Vị trí cuối vùng theo định dạng thời gian đã chọn',
    'New Range End Position in Selected Time Format':
        'Vị trí cuối vùng mới theo định dạng thời gian đã chọn',
    'New Range Length in Selected Time Format':
        'Độ dài vùng mới theo định dạng thời gian đã chọn',
    'Range in Primary Time Format':
        'Vùng theo Primary Time Format',

    # 19. Info Line / Status Line
    'Info Line':
        'Info Line',
    'Set up Info Line':
        'Thiết lập Info Line',
    'Show Info Line':
        'Hiện Info Line',
    'Status Line':
        'Status Line',
    'Show/Hide Status Line':
        'Hiện/Ẩn Status Line',
    'Overview Line':
        'Overview Line',

    # 20. Tautologies / Skins / Theme / Computer
    'Skins':
        'Skin',
    'Theme':
        'Theme',
    'This Computer':
        'Máy tính này',
    "Doesn't seem to be a valid skin file!":
        'Đây có vẻ không phải là file Skin hợp lệ!',

    # 21. Queue / Job / Pool / Link Group
    'Export Queue':
        'Hàng đợi Export',
    'Add Job to Queue':
        'Thêm tác vụ vào hàng đợi',
    'Start Queue Export':
        'Bắt đầu Export hàng đợi',
    'Remove Job':
        'Gỡ bỏ tác vụ',
    'Update Job':
        'Cập nhật tác vụ',
    "To save your changes for the selected job, please click 'Update Job'.":
        "Để lưu các thay đổi cho tác vụ đã chọn, vui lòng nhấp 'Cập nhật tác vụ'.",
    'Find Selected in Pool':
        'Tìm mục đã chọn trong Pool',
    'Set Pool Record Folder':
        'Đặt thư mục ghi âm của Pool',
    'Pool Record Folder':
        'Thư mục ghi âm của Pool',
    'Pool Record Folder:':
        'Thư mục ghi âm của Pool:',
    'Remove Channel from Link Group "%s"':
        'Gỡ bỏ Channel khỏi Link Group "%s"',
    'Remove VCA Channel from Link Group "%s"':
        'Gỡ bỏ VCA Channel khỏi Link Group "%s"',
    'Link Group':
        'Link Group',
    'Unlink Channels':
        'Hủy liên kết các Channel',
    'Unlink Selected Channels':
        'Hủy liên kết các Channel đã chọn',
    'Add Selected as MMC Slaves':
        'Thêm các mục đã chọn làm MMC Slave',
    'Add Selected as Remote Slaves':
        'Thêm các mục đã chọn làm Remote Slave',
    'Import video events as marker?':
        'Import các Video Event làm Marker?',

    # 22. Misc UI and Audio consistency
    'Click during Count-In':
        'Click trong lúc Count-In',
    'Start Preview Mode':
        'Bắt đầu chế độ Preview',
    'Set Preview Start to Cursor':
        'Đặt điểm bắt đầu Preview tại Cursor',
    'Fill View[Score View Option]':
        'Chế độ xem: Fill View',
    'Start Time':
        'Thời gian bắt đầu',
    'Start Position':
        'Vị trí bắt đầu',
    'Show/Hide Direct Routing':
        'Hiện/Ẩn Direct Routing',
    'Show Routing as <%s>':
        'Hiện Routing dạng <%s>',
    'Are you sure you want to deactivate all cue sends?':
        'Bạn có chắc muốn tắt tất cả Cue Send không?',
    'Activate Cue Sends':
        'Bật Cue Send',
    'Deactivate Cue Sends':
        'Tắt Cue Send',
    'Reset All Cue Sends':
        'Đặt lại tất cả Cue Send',
    'Open Modulators in Window':
        'Mở các Modulator trong Window',
    'Show Modulators in Lower Zone':
        'Hiện các Modulator trong Lower Zone',
    'Export list as text':
        'Export danh sách dưới dạng văn bản',
    'Export Key Command Assignments':
        'Export phím tắt đã gán',
    'Key Command Assignments...':
        'Các phím tắt đã gán...',
    'Initial assignment of input movements to VST Note Expressions':
        'Gán ban đầu các thao tác đầu vào cho VST Note Expression',
    'Replace Audio in Project':
        'Thay thế Audio trong Project',
    'Replace Audio in Video':
        'Thay thế Audio trong Video',
    'Replace Audio in Video File...':
        'Thay thế Audio trong file Video...',
    'New + Replace in Pool':
        'Mới + Thay thế trong Pool',
    'Replacement of PFX':
        'Thay thế PFX',
    'Set Transparency for Comparison Channel Curve':
        'Đặt độ trong suốt cho đường cong Channel so sánh',
    'Transparency for Comparison Channel Curve:':
        'Độ trong suốt cho đường cong Channel so sánh:',
    'EQ Comparison Channel':
        'Channel so sánh EQ',
    'No Comparison Channel':
        'Không có Channel so sánh',
    'Send Destination, Gain & Send Controls':
        'Đích Send, Gain & Điều khiển Send',
    'Select MIDI Send Destination':
        'Chọn đích của MIDI Send',
    'Send Destination & Gain (Compact)':
        'Đích Send & Gain (Gọn)',
    'Import Master Track':
        'Import Master Track',
    'Project Templates':
        'Project Template',
    'Without Channel Settings (Transfer All Settings from Source to New Track)':
        'Không kèm cài đặt Channel (Chuyển tất cả cài đặt từ nguồn sang Track mới)',
    'Render Audio Click between Locators':
        'Render Audio Click giữa hai Locator',
    'Render MIDI Click between Locators':
        'Render MIDI Click giữa hai Locator',
    'New Audio Drivers Found':
        'Tìm thấy Driver Audio mới',
    'New Sample Rate':
        'Sample Rate mới',
    'HW Sample Rate':
        'Sample Rate phần cứng',
    'New MIDI Loop':
        'MIDI Loop mới',
    'New VCA Channel':
        'VCA Channel mới',
    'Deactivate all third party plug-ins':
        'Tắt tất cả Plug-in bên thứ ba',
    'External Plug-ins':
        'Các Plug-in ngoài',
    'Save Plug-in Report':
        'Lưu báo cáo Plug-in',
    'Open Plug-in Manager':
        'Mở Plug-in Manager',
    'Show/Hide Plug-ins':
        'Hiện/Ẩn Plug-in',
    'Show/Hide VST Plug-in Pictures':
        'Hiện/Ẩn hình ảnh VST Plug-in',
    'Routing with Plug-in Picture':
        'Routing kèm hình ảnh Plug-in',
    'Add VST Plug-in Picture to Media Rack':
        'Thêm hình ảnh VST Plug-in vào Media Rack',
    'Apply MIDI Velocity Variance':
        'Áp dụng độ biến thiên Velocity MIDI',
    'Reset MIDI Velocity Variance':
        'Đặt lại độ biến thiên Velocity MIDI',
    'Set Velocity Variance':
        'Đặt độ biến thiên Velocity',
    'Punch Points':
        'Punch Point',
    'Show/Hide Chord Pads':
        'Hiện/Ẩn Chord Pad',
    'Insert Selected In Arranger Chain':
        'Chèn mục đã chọn vào Arranger Chain',
    'Rename Arranger Events':
        'Đổi tên Arranger Event',
    'Extract Markers from Wave File':
        'Trích xuất Marker từ file Wave',
    'Extract Sound from Track Preset':
        'Trích xuất Sound từ Track Preset',
    'Project Preview start set to project cursor position.':
        'Điểm bắt đầu của Project Preview được đặt tại vị trí con trỏ Project.',
    'It is not possible to create a shared copy if the timebase of the tracks do not match.\\nA real copy was created instead.':
        'Không thể tạo bản sao chia sẻ nếu Timebase của các Track không khớp.\\nMột bản sao độc lập đã được tạo để thay thế.',
    'An exception occurred. Save your work and restart the application.\\nThe exception was thrown because of the plug-in :\\n\\n':
        'Đã xảy ra lỗi ngoại lệ. Hãy lưu công việc của bạn và khởi động lại ứng dụng.\\nLỗi phát sinh do Plug-in :\\n\\n',
    'Auto Save failed, because the project is corrupt.\\nPlease save the project under a new name and restart the program.':
        'Không thể tự động lưu vì Project bị hỏng.\\nVui lòng lưu Project dưới một tên mới và khởi động lại chương trình.',
    'Conversion failed!':
        'Chuyển đổi không thành công!',
    'Data Transfer failed.\\nTo avoid data loss, the data will remain in source database.\\n':
        'Không thể chuyển dữ liệu.\\nĐể tránh mất dữ liệu, dữ liệu sẽ được giữ lại trong cơ sở dữ liệu nguồn.\\n',
    'Database creation failed because the target is write protected.\\n':
        'Không thể tạo cơ sở dữ liệu vì đích bị bảo vệ ghi.\\n',
    'Database removal failed because the data could not be transferred.':
        'Không thể xóa cơ sở dữ liệu vì không truyền được dữ liệu.',
    'Database removal failed because the database file is write protected.\\n':
        'Không thể xóa cơ sở dữ liệu vì file cơ sở dữ liệu bị bảo vệ ghi.\\n',
    'Processing Failed':
        'Xử lý không thành công',
    'Reactivating the plug-in failed!\\nFor support information, please contact the plug-in vendor.':
        'Không thể kích hoạt lại Plug-in!\\nĐể biết thông tin hỗ trợ, vui lòng liên hệ nhà cung cấp Plug-in.',
    'The quick loudness analysis failed. An internal error occurred.':
        'Phân tích Loudness nhanh không thành công. Đã xảy ra lỗi nội bộ.',
    'Unpack Project Failed!':
        'Không thể giải nén Project!',
    'Verify failed for this node!':
        'Xác minh không thành công cho node này!',
    'Skin parsing failed':
        'Phân tích file Skin không thành công',
    'Follow Beat Grouping':
        'Bám theo cách gom nhóm phách',
    'Note Grouping':
        'Gom nhóm Note',
    'All Multi-Channel Tracks':
        'Tất cả các Track đa kênh',
    'Split Multi-Channel Tracks':
        'Tách các Multi-Channel Track',
    'Import Position for New Tracks':
        'Vị trí Import cho các Track mới',
    'Import Controller as Automation Tracks':
        'Import Controller làm Automation Track',
    'Import Track Picture':
        'Import hình ảnh Track',
    'Import Position':
        'Vị trí Import',
    'Import Karaoke Lyrics as Text':
        'Import lời Karaoke dưới dạng văn bản',
    'Import Key Switches from Instrument':
        'Import Key Switch từ Instrument',
    'Markers Window':
        'Cửa sổ Marker',
    'Open Markers Window':
        'Mở cửa sổ Marker',
    'Insert Chord Notes':
        'Chèn các nốt hợp âm',
    'VCA Settings Options':
        'Tùy chọn cài đặt VCA',
    'Send machine control commads to selected SyncStation port':
        'Gửi lệnh Machine Control tới cổng SyncStation đã chọn',
    'Set Channel Type Filter\\nUse [CTRL + click] to Reset Channel Type Filter':
        'Thiết lập bộ lọc loại Channel\\nDùng [CTRL + nhấp chuột] để đặt lại bộ lọc loại Channel',
    'Set Channel Visibility Agents\\nUse [ALT]-Click to Reset Channel Visibility Agents':
        'Thiết lập Channel Visibility Agent\\nDùng [ALT] + nhấp chuột để đặt lại Channel Visibility Agent',
    'Edit Pitch':
        'Sửa Pitch',
    'Set Pitch':
        'Đặt Pitch',
    'Highest Pitch':
        'Pitch cao nhất',
    'Lowest Pitch':
        'Pitch thấp nhất',
    'Original Pitch':
        'Pitch gốc',
    'Original Segment Pitch':
        'Pitch gốc của Segment',
    'Separate Pitches':
        'Tách riêng các Pitch',
    'Quantize Pitches to Scale':
        'Quantize Pitch theo Scale',
    'Show Pitches with Events':
        'Hiện Pitch có Event',
    'Sort Lanes by Pitch':
        'Sắp xếp Lane theo Pitch',
    'Transposed Pitch':
        'Pitch đã Transpose',
    'Vertical Pitch Spread':
        'Độ phân bố Pitch theo chiều dọc',
    'Create Groove Quantize Preset from Hitpoints':
        'Tạo Preset Groove Quantize từ Hitpoint',
    'Notes Starting on a Beat Followed by a Rest in the Middle of the Beat':
        'Các nốt bắt đầu tại phách và theo sau là dấu lặng ở giữa phách',
    'Notes Starting on a Beat Ending in the Middle of the Beat':
        'Các nốt bắt đầu tại phách và kết thúc ở giữa phách',
    'Cross Staff: Cross to Staff Above':
        'Chuyển khuông: Đưa lên khuông nhạc trên',
    'Cross Staff: Cross to Staff Below':
        'Chuyển khuông: Đưa xuống khuông nhạc dưới',
    'Cross Staff: Move to Staff Above':
        'Chuyển khuông: Di chuyển lên khuông trên',
    'Cross Staff: Move to Staff Below':
        'Chuyển khuông: Di chuyển xuống khuông dưới',
    'Cross Staff: Reset to Original Staff':
        'Chuyển khuông: Đặt lại về khuông gốc',
    'Show Normal Bar Number If Coincident with Start of Multi-Bar Rest Showing Range':
        'Hiện số Bar thông thường nếu trùng với đầu dải dấu lặng nhiều Bar',
    'Show Ranges of Bar Numbers Under Multi-Bar Rests and Consolidated Bar Repeats':
        'Hiện dải số Bar dưới dấu lặng nhiều Bar và ký hiệu lặp Bar gộp',
    'Default Warping Algorithm':
        'Thuật toán Warping mặc định',
    'Warping Algorithm for Audio Clip':
        'Thuật toán Warping cho Audio Clip',
    'Open Direct Offline Processing Window':
        'Mở cửa sổ Direct Offline Processing',
    'Open Sampler Control Window':
        'Mở cửa sổ Sampler Control',
    'Open Naming Scheme Window':
        'Mở cửa sổ Naming Scheme',
    'Naming Scheme - Channel Batch Arranger Chain':
        'Quy tắc đặt tên - Channel Batch Arranger Chain',
    'Naming Scheme - Single Channel Arranger Chain':
        'Quy tắc đặt tên - Single Channel Arranger Chain',
    'Set Audio Signature':
        'Đặt số chỉ nhịp của Audio',
    'Paste Click Pattern to Selected Signatures':
        'Dán Click Pattern vào các số chỉ nhịp đã chọn',
    'Remote Trigger Mode: Use either key switches or program changes to switch between Sound Slots':
        'Chế độ kích hoạt Remote: Dùng Key Switch hoặc Program Change để chuyển đổi giữa các Sound Slot',
    'Expression Maps':
        'Các Expression Map',
    'Expression Map: Articulations':
        'Expression Map: Articulation',
    'Import MIDI Devices':
        'Import các MIDI Device',
    'Export MIDI Device Setup':
        'Export thiết lập MIDI Device',
    'Import MIDI Device Setup':
        'Import thiết lập MIDI Device',
    'Exporting Track Nr: %d ...':
        'Đang Export Track số: %d...',
    'Import audio tracks from video':
        'Import Audio Track từ Video',
    'VST 2 Plug-in Path Settings':
        'Cài đặt đường dẫn VST 2 Plug-in',
    'Reset FFT Post EQ Peak Hold Curve':
        'Đặt lại đường cong giữ đỉnh FFT Post EQ',
    'Delay in ms':
        'Delay tính bằng ms',
    'Delay':
        'Delay',
    'Audio in musical mode cannot be sliced.\\nDo you want to disable musical mode?':
        'Audio ở chế độ Musical không thể cắt thành Slice.\\nBạn có muốn tắt chế độ Musical không?',
    'Sliced audio cannot be switched to musical mode.':
        'Audio đã tạo Slice không thể chuyển sang chế độ Musical.',
    "'%s' is not supported for clips in musical mode!":
        "'%s' không được hỗ trợ cho Clip ở chế độ Musical!",
}

real = {k: v for k, v in WORDING.items() if k in src}
missing = sorted(set(WORDING) - set(real))
if missing:
    print(f'NOT IN CUBASE ({len(missing)}):')
    for m in missing:
        print(f'  {m!r}')
    print()

bad = [(k, v) for k, v in real.items()
       if sorted(PH.findall(src[k])) != sorted(PH.findall(v))
       or '\ufffd' in v or not v.strip() or '[RM]' in v
       or src[k].count('\\n') != v.count('\\n')]
if bad:
    print('PROBLEM (placeholder, U+FFFD, empty, [RM], or line breaks):')
    for k, v in bad:
        print(f'  {k!r}\n      src {src[k]!r}\n   ->  {v!r}')
    sys.exit(1)

changed = {k: v for k, v in real.items() if vi.get(k) != v}
print(f'hand-written keys : {len(real)}')
print(f'total to change  : {len(changed)}\n')
for k, v in list(changed.items())[:20]:
    print(f'  {k[:58]!r}')
    print(f'      {vi.get(k, "")[:110]!r}')
    print(f'   -> {v[:110]!r}')

if not WRITE:
    print('\n(dry run - pass --write)')
    sys.exit(0)

n = 0
for path in sorted(glob.glob(os.path.join(BATCH_DIR, '*.json'))):
    data = json.load(open(path, encoding='utf-8'))
    dirty = False
    for k, v in changed.items():
        if k in data and data[k] != v:
            data[k] = v
            dirty = True
            n += 1
    if dirty:
        json.dump(data, open(path, 'w', encoding='utf-8'),
                  ensure_ascii=False, indent=2, sort_keys=True)

print(f'\nupdated {n} batch occurrences across {len(glob.glob(os.path.join(BATCH_DIR, "*.json")))} files')
