# PiMove
※以下の処理はWindows環境用です。MACやLinux環境ではでの動作は保証できません

【導入】
まず、MinGWをインストールします
https://github.com/niXman/mingw-builds-binaries/releases

そしたらPictureModifier3.pyの2行目にある
os.add_dll_directory(r"bin path")
という部分を、インストールした場所のbinファイルに設定してください

次にCMakeを導入します


cmake -Wno-dev -G "MinGW Makefiles" -DCMAKE_C_COMPILER:FILEPATH="C:/mingw64/bin/gcc.exe" -DCMAKE_CXX_COMPILER:FILEPATH="C:/mingw64/bin/g++.exe" -DCMAKE_MAKE_PROGRAM="C:/mingw64/bin/mingw32-make.exe" .

cmake --build .

