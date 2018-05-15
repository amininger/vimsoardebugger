""""""""""""""""" Soar Plugin Commands """""""""""""""""""

" Commands for using the soar debugger
command! -nargs=0 CloseDebugger :Python close_debugger()
command! -nargs=0 ResetDebugger :Python reset_debugger()

" Source the current file into the running soar agent (debugger.vim)
command! -nargs=0 SourceCurrentFile :call ExecuteSoarCommand("source ".expand('%:p'))

" Source a specified file into the running soar agent (debugger.vim)
command! -nargs=1 -complete=file SourceSoarFile :call SourceSoarFile(<f-args>)

""""""""""""""""" Soar Plugin Key Mappings """""""""""""""""""

" If you set the global variable enable_soar_plugin_mappings to 0
" the plugin keybindings will be skipped
if !exists('g:enable_soar_plugin_mappings')
	let g:enable_soar_plugin_mappings = 1
endif
if !g:enable_soar_plugin_mappings
	finish
endif

" Execute an arbitrary soar command
nnoremap # :call ExecuteUserSoarCommand()<CR>

nnoremap H :Python step(1)<CR>
nnoremap U :Python step(10)<CR>
" Run 1 elaboration cycle
nnoremap ;re :Python agent.execute_command("run 1 -e")<CR>

" See which rules currently match
nnoremap ;ma :Python agent.execute_command("matches")<CR>

" source production
nnoremap ;sp :call ExecuteSoarCommand(GetCurrentSoarRuleBody())<CR>
" matches production
nnoremap ;mp :call ExecuteSoarCommand("matches ".GetCurrentSoarRuleName())<CR>
" excise production
nnoremap ;ep :call ExecuteSoarCommand("excise ".GetCurrentSoarRuleName())<CR>

" print rule by name
nnoremap ;pr :call ExecuteSoarCommand("p ".GetStrippedCurrentWord())<CR>
" matches rule name
nnoremap ;mr :call ExecuteSoarCommand("matches ".GetStrippedCurrentWord())<CR>
" excise rule name
nnoremap ;er :call ExecuteSoarCommand("excise ".GetStrippedCurrentWord())<CR>

" print wmes
nnoremap ;p1 :<C-U>call ExecuteSoarCommand("p ".GetStrippedCurrentWord())<CR>
nnoremap ;p2 :<C-U>call ExecuteSoarCommand("p ".GetStrippedCurrentWord()." -d 2")<CR>
nnoremap ;p3 :<C-U>call ExecuteSoarCommand("p ".GetStrippedCurrentWord()." -d 3")<CR>
nnoremap ;p4 :<C-U>call ExecuteSoarCommand("p ".GetStrippedCurrentWord()." -d 4")<CR>
nnoremap ;p5 :<C-U>call ExecuteSoarCommand("p ".GetStrippedCurrentWord()." -d 5")<CR>
nnoremap ;p6 :<C-U>call ExecuteSoarCommand("p ".GetStrippedCurrentWord()." -d 6")<CR>
nnoremap ;p7 :<C-U>call ExecuteSoarCommand("p ".GetStrippedCurrentWord()." -d 7")<CR>
nnoremap ;p8 :<C-U>call ExecuteSoarCommand("p ".GetStrippedCurrentWord()." -d 8")<CR>
nnoremap ;p9 :<C-U>call ExecuteSoarCommand("p ".GetStrippedCurrentWord()." -d 9")<CR>

