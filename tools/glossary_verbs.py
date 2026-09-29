#!/usr/bin/env python3
"""Fix "Không thể <Verb>" strings.

Two defects in one family:
  * the verb was left capitalised mid-sentence, which in Vietnamese marks a
    proper noun - "Không thể Tạo file" reads as if "Tạo" were a name
  * the object was often left in English - "Không thể Thêm tracks while
    recording", "Không thể Tạo Ghi file!"
"""

WORDING = {
    'Cannot Edit VariAudio: No Note Segments Detected':
        'Không thể sửa VariAudio: Không phát hiện đoạn Note nào',
    'Cannot add tracks while recording.':
        'Không thể thêm Track trong lúc đang ghi.',
    'Cannot create split file': 'Không thể tạo file chia nhỏ',
    'Cannot import this image!': 'Không thể Import hình ảnh này!',
    'Cannot open media: %s': 'Không thể mở media: %s',
    'Cannot open project file "%s" !': 'Không thể mở file Project "%s" !',
    'Could not create Clip Packages directory!':
        'Không thể tạo thư mục Clip Packages!',
    'Could not create OMF file...': 'Không thể tạo file OMF...',
    'Could not create audio directory!': 'Không thể tạo thư mục Audio!',
    'Could not create file': 'Không thể tạo file',
    'Could not create file.\\n%s': 'Không thể tạo file.\\n%s',
    'Could not create link for:\\n': 'Không thể tạo liên kết cho:\\n',
    'Could not create project directory!': 'Không thể tạo thư mục Project!',
    'Could not create record file!': 'Không thể tạo file ghi!',
    'Could not import all resources!': 'Không thể Import tất cả tài nguyên!',
    'Could not import all tracks! The data is corrupted.':
        'Không thể Import tất cả Track! Dữ liệu bị hỏng.',
    'Could not import the Clip Package! The data is corrupt.':
        'Không thể Import gói Clip! Dữ liệu bị hỏng.',
    'Could not load GUI Resources!\\n': 'Không thể tải tài nguyên Giao diện!\\n',
    'Could not open URL': 'Không thể mở URL',
    'Could not open file': 'Không thể mở file',
    'Could not save skin file!': 'Không thể lưu skin file!',
    'Export is not possible with an empty project.':
        'Không thể Export với một Project trống.',
    'Script Archive could not be imported.':
        'Không thể Import kho lưu trữ Script.',
    'Script could not be exported.': 'Không thể Export Script.',
    'The selected track types cannot be exported!':
        'Không thể Export các loại Track đã chọn!',
    'The track archive cannot be imported!':
        'Không thể Import gói Track đã lưu!',
    'WARNING: Cannot import video files!':
        'CẢNH BÁO: Không thể Import file Video!',
}
