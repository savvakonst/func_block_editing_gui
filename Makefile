


#LEXER_FILENAMES=calc_lexer.go calc_parser.go calc_listener.go

#INCLUDE_PATHS=C:\Python27\include
INCLUDE_PATHS=C:\Users\SVK\AppData\Local\Programs\Python\Python38\include


#LIB_PATHS=C:\Python27\libs
LIB_PATHS=C:\Users\SVK\AppData\Local\Programs\Python\Python38\libs

all:
	$(CXX) -c       scene.cpp              -I $(INCLUDE_PATHS) -D MS_WIN64   -std=c++11
	$(CXX) -shared scene.o -o scene.pyd    -L $(LIB_PATHS)     -l Python38   -std=c++11


small:
	gcc -c libmypy.c -IC:\Users\{user_name}\Anaconda3\pkgs\python-3.6.4-h6538335_1\include
	gcc -shared -o libmypy.dll libmypy.o  -LC:\Users\{user_name}\Anaconda3\pkgs\python-3.6.4-h6538335_1\libs -lPython36