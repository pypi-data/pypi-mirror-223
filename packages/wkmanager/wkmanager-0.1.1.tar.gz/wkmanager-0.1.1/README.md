
# Welcome to WkManager!

An unnoficial lib that facilitates the download of wkhtmltopdf/wkhtmltoimage (wkhtmltox), based on the characteristics of the system such as OS, architecture of the processor and also the availability of the software, also being possible to manually select this information.

# WkManager

A class to validation of system characteristics to start downloading wkhtmltopdf/wkhtmltopdf (wkhtmltox) files from the official website (please consult directly for more information).
### Attributes

| Attribute | Type |
| -------- | ----- |
| sys      |**str**|
| support  |**str**|
| arch     |**str**|
| extension|**str**|

- **system**: the OS you are looking for, if None will be replace by checking your OS.

- **support**: the support are looking for, like "XP", "Vista", "Debian", "Arch. if None wil be replaced by checking your OS.

- **arch**: the OS architecture you are looking for, if None will be replace by checking your machine.

- **extension**: the extension you looking for, if None will raise an ValueError with the avaliable extensions for you based on others attributes.

Example:
```
from wkmanager import WkManager

Wk = WkManager("Windows", "XP", "64bit", "7z")
```
>If successful, you can use the **get_wk** method.


## get_wk

Method to download the wkhtmltox files, being able to unzip it automatically (winrar required for 7z files).

### Args

|Attribute|         Type |
| --------|--------------|
| path          | **str**|
| extract       |**bool**|
| winrar_path   | **str**|

- **path**: the path where the file will be saved, if None will saved on root.

- **extract**: if True, the file will be extracted if it is 7z or Zip, by default it is False.

- **winrar_path**: if a 7z file extension is selected and extract is True, it will be necessary to have Winrar installed and pass the path to winrar.exe for the file to be unpacked.

```
from wkmanager import WkManager

Wk = WkManager("Windows", "XP", "64bit", "7z")
wk_path = Wk.get_wk("wk_folder", True, "C:\Program Files\WinRAR\WinRAR.exe")
```

>the if extract is True, the file will be full unpacked without internal folder.

### Returns
Returns the path of folder with wk files.
