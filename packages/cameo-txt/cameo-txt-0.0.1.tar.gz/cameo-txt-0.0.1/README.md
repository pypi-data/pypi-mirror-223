# cameo-txt

`cameo-txt` 是一個用於將不同檔案格式（如 docx、pdf、csv、odt 等）轉換為純文本文件的 Python 庫。

## 安裝

您可以使用以下命令安裝此套件：

```bash
pip install cameo-txt
```
## 用法
以下是一個簡單的例子，說明如何使用這個函數庫：

```
from cameo_txt import convert_to_txt

# 單個檔案
result = convert_to_txt('path/to/your/file.docx')

# 多個檔案
results = convert_to_txt(['path/to/your/file1.pdf', 'path/to/your/file2.csv'])

# 保存到特定輸出資料夾
results = convert_to_txt(['path/to/your/file1.pdf', 'path/to/your/file2.csv'], output_folder='path/to/output/folder')
```
## 功能
cameo-txt主要提供以下功能：
### 下載文件
如果提供了URL，庫將自動下載文件並保存為臨時文件。
### 支援多種格式
支援docx、pdf、csv和odt格式的文件。您可以輕鬆添加對更多格式的支援。
### 並行處理
使用concurrent.futures並行處理多個文件，以提高效率。
### 自動編碼檢測
使用chardet自動檢測和處理不同編碼的文件。