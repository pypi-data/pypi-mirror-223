
emsdk-env emcc  \
	-Os -DMAKE_LUA_WASM -DLUA_PROGNAME='"lua"' \
	-DLUA_USE_LINUX -D_XOPEN_SOURCE=500 \
	-o am-lua-5.4.4.js *.c \
	-sEXPORTED_FUNCTIONS=_run_lua -sEXPORTED_RUNTIME_METHODS=ccall,cwrap \
	-sALLOW_MEMORY_GROWTH \

#--embed-file $HOME/dev/lua/lpeglabel/relabel.lua@$destFolder \
#--embed-file $HOME/dev/lua/lpegrex/lpegrex.lua@$destFolder

