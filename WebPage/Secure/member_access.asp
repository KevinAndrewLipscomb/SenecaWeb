<% Response.Buffer=true %>
<html>

<head>
<meta http-equiv="Content-Type" content="text/html; charset=windows-1252">
<meta name="GENERATOR" content="Microsoft FrontPage 4.0">
<meta name="ProgId" content="FrontPage.Editor.Document">
<title>Member Access</title>
</head>

<body>
<% If Request.Form("pw") = "parkviewsucks" Then %>
<p align="center">members area</p>
<p align="center">&nbsp;</p>
<p align="center">&nbsp;</p>
<p align="center">&nbsp;</p>
<p align="center">to be defined</p>
<% Else
Response.Write "To view this page, enter a valid password." & _
"<FORM ACTION=""thispage.asp"" METHOD=""POST"">" & _
"<INPUT SIZE=10 TYPE=""password"" NAME=""pw"">" & _
"<INPUT TYPE=""submit"" NAME=""Submit"" VALUE=""Go"">"  & _
"</FORM>"
End If %>
</body>

</html>
