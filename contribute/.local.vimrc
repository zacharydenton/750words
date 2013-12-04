function! WordCount()
let s:old_status = v:statusmsg
let position = getpos(".")
exe ":silent normal g\<c-g>"
let stat = v:statusmsg
let s:word_count = 0
  if stat != '--No lines in buffer--'
    if stat =~ "^Selected"
    let s:word_count = str2nr(split(v:statusmsg)[5])
    else
    let s:word_count = str2nr(split(v:statusmsg)[11])
    end
  let v:statusmsg = s:old_status
  end
call setpos('.', position)
return s:word_count
endfunction

:set statusline=wc:%{WordCount()}\ words\ 
