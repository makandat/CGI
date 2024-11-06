<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8" />
  <title>${title}</title>
  <link rel="stylesheet" href="/css/style.css" />
  <style>
   #d {
     margin-left:30%;
     margin-top:40px;
     font-size:larger;
   }
  </style>
 </head>
 
 <body>
  <h1>${title}</h1>
  <div id="d">
  <ul>
  % for i in r6:
    % if i % 2 == 0:
    <li style="color:red;">${i} Even</li>
    % else:
    <li style="color:blue;">${i} Odd</li>    
    % endif
  % endfor
  </ul>
  </div>
 </body>
</html>
