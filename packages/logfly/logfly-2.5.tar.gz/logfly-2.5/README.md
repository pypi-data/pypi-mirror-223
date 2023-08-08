# logfly  2.4  
### a simple log tool by python.  

## position  
log will create in ./logs/[folder_name]/[date] folder.  
if use hidden, log will also appear in user/.1o9f1y folder.  

## How to  
### import  
    import logfly  
### write_log    
    logfly.write_log('name', 'where', 'info', 'message', mode='add', folder_name='default-log', hidden='no', color='yes', str_message='yes')  

#### Description  
    name: (any str) logfile name, you can use diffrent string to create diffrent logfile.  
    where: ('CLI', 'fileCLI', 'file') position where log appear.  
            fileCLI means log will appear in command line window and log file.  
            CLI means log will only appear in command line window.  
            file means log will only appear in logfile.  
    info: (any str) custom log level, will upper and wrap with '[]'.  
    message: (any str) log message.  
    mode: ('add', 'new') default is 'add', means log will add in same day.  
            'new' means logfile will create when program every once.
    folder_name: (any str) custom logfly folder name, default is 'default-log'.  
    hidden: ('yes', 'no') default is 'no', means logfile will save a copy in user/.1o9f1y folder  
    color: ('yes', 'no') default is 'yes', means log will with color.  
    str_message: ('yes', 'no') default is 'yes', means log will print message with str()  

### create_or_check_file  
    create_or_check_file(pathorfile, name, warning='yes'): 
        create or check file.  
        pathorfile: ('file', 'path') choose to create file or path.  
        name: (any str) file or path name.  
        if warning is 'yes', will print warning message if file or path is exist.  

#### Description  
    pathfile is the file path that you want to create, must fill with '//'  
    filenname is the file name that you want to create, must is with '*.*'  
