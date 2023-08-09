from concurrent.futures import ProcessPoolExecutor
import os
import requests
import tempfile
import mimetypes
from urllib.parse import urlparse, unquote
from .converters.docx_converter import convert_docx_to_txt
from .converters.pdf_converter import convert_pdf_to_txt
from .converters.csv_converter import convert_csv_to_txt
from .converters.odt_converter import convert_odt_to_txt
#from .converters.doc_converter import convert_doc_to_txt
# 其他的導入...

def _download_file(url):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to download file from {url}")
    content_type = response.headers.get('Content-Type')
    #print(response.headers)
    #print('content_type:', content_type)
    content_disposition = response.headers.get('Content-Disposition')
    if content_disposition:
        filename_key = 'FileName='
        start_idx = content_disposition.find(filename_key)
        if start_idx != -1:
            filename = content_disposition[start_idx + len(filename_key):]
            filename = unquote(filename)  # 解码URL编码的字符
            suffix = os.path.splitext(filename)[1]
            print('Extracted filename:', filename)
            print('Extracted suffix:', suffix)
    else:
        suffix = mimetypes.guess_extension(content_type)
        if content_type.lower() == 'application/octet-stream':
            path = urlparse(url).path
            suffix = os.path.splitext(path)[1]
            print("Extracted suffix from URL:", suffix)
    #print(suffix)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    with temp_file as f:
        f.write(response.content)
    return temp_file.name

def _process_file(file_path, output_folder=None):
    try:
        # 檢查是否是網路URL
        if file_path.startswith('http'):
            # 嘗試下載文件並保存到臨時文件中
            file_path = _download_file(file_path)
        elif not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        file_extension = file_path.split('.')[-1].lower()

        converters = {
            'docx': convert_docx_to_txt,
            #'doc': convert_doc_to_txt,
            'pdf': convert_pdf_to_txt,
            'csv': convert_csv_to_txt,
            'odt': convert_odt_to_txt,
            # 其他的格式...
        }

        convert_func = converters.get(file_extension)
        
        if convert_func:
            result = convert_func(file_path)

            # 如果設置了輸出資料夾，則保存結果到該資料夾
            if output_folder:
                # 確保輸出資料夾存在
                os.makedirs(output_folder, exist_ok=True)
                
                # 創建輸出文件名稱
                output_filename = os.path.join(output_folder, os.path.basename(file_path) + ".txt")
                
                # 將結果保存到文件
                with open(output_filename, 'w') as output_file:
                    output_file.write(result)
            if file_path.startswith(tempfile.gettempdir()):
                os.unlink(file_path)
            return result
        else:
            print(f'Unsupported file extension {file_extension}.')
            raise ValueError(f'Unsupported file extension {file_extension}.')
    except Exception as e:
        print(f"An error occurred with file {file_path}: {str(e)}")
        return None  # 可以添加None或自定義的錯誤訊息

def convert_to_txt(file_paths, output_folder=None):
    if isinstance(file_paths, str):
        file_paths = [file_paths]

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(_process_file, file_paths, [output_folder] * len(file_paths)))

    return results
