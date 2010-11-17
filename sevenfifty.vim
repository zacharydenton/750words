" word count functions
function WordCount()
	let s:old_status = v:statusmsg
	exe "silent normal g\<c-g>"
	let s:word_count = str2nr(split(v:statusmsg)[11])
	let v:statusmsg = s:old_status
	return s:word_count
endfunction

set statusline=wc:%{WordCount()}

" word wrap options
set wrap
set linebreak
