#!/usr/local/bin/perl
# Remember that the above line has to reflect where your perl really resides.  This is a
# simple form handler that uses form values to send mail to a hard-coded user.

# Terminate headers
print  "Content-type: text/html\n\n";

# Who should get the email and where is the email program?
$send_to = "seneca\@icubed.com"; 
$mail_prog = "/usr/sbin/sendmail";

# See if the user sent an HTTP_FROM header.  Many clients don't these days.
$http_from = $ENV{"HTTP_FROM"};

# See which method they used to access this form.  If they used POST, then
# read the input from STDIN.  If they used GET, use the query string.

# Which method is used is determined by the HTML in the form.
if($ENV{'REQUEST_METHOD'} eq "GET") {
  $buffer = $ENV{'QUERY_STRING'};
  if($buffer eq "")  {
    print "<HTML>\n";
    print "  <HEAD>\n";
    print "    <TITLE>Sorry - Use HTML Form\!</TITLE>\n";
    print "  </HEAD>\n";
    print "  <BODY BGCOLOR=\"FFFFFF\">\n";
    print "    <H2 ALIGN=\"center\">Please use the HTML Form Provided\!</H2>\n";
    print "    <HR SIZE=5>\n";
    print "    <P>\n";
    print "<TITLE>Error - use HTML</TITLE>\n";
    print "You accessed this program without a valid query string. Please ";
    print "use the associated HTML form to access it.\n";
    print "    <P>\n";
    print "    <HR SIZE=5>\n";
    print "    <P>\n";
    print "  </BODY>\n";
    print "</HTML>\n";
    exit(1);
  }
}  else  {
  read(STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
}

# Split pairs by the ampersand which divides variables
@pairs = split(/&/, $buffer);
# Create an array, indexed by the variable name, that contains all the values
foreach $pair (@pairs)
{
# Each variable is structured "namel=valuel", so split it on those lines
  ($name, $value) = split(/=/, $pair);

# Decode the value (+ is a space, and %xx in hex is an encoded character)
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
# Create an array indexed by names and put the value in
  $form{$name} = $value;
}

# We should have the following values:
#  email  = the person's email address
#  p_feed = the person's positive feedback
#  n_feed = the person's negative feedback
#
# Next, we need to put it into a usable form and mail it.  Check to see if they left
# an email address.  We don't check to see if it's valid, just to see if it's there.
if($form{"email"} eq "")   {
  print "<HTML>\n";
  print "  <HEAD>\n";
  print "    <TITLE>Sorry - We need an E-Mail Address\!</TITLE>\n";
  print "  </HEAD>\n";
  print "  <BODY BGCOLOR=\"FFFFFF\">\n";
  print "    <H2 ALIGN=\"center\">We Need an E-Mail Address</H2>\n";
  print "    <HR SIZE=10>\n";
  print "    <P>\n";
  print "Your request could not be sent because you ";
  print "did not supply an E-Mail address.  Please enter an E-Mail ";
  print "address and try again.\n";
  print "    <P>\n";
  print "    <HR SIZE=10>\n";
  print "    <P>\n";
  print "  </BODY>\n";
  print "</HTML>\n";
  exit(1);
}

# Open the mail command, or print an error.
open (MAIL, "|$mail_prog $send_to") || die "Could not open $mail_prog";

# Send the feedback.  If the user had an HTTP_FROM variable, use that in
# the from line.  If not, use the one he gave in the form.
if($http_from)
  { print MAIL "From: $http_from\n"; }
else
  { print MAIL "From: $form{'e_mail_address'}\n"; }

# Print their email address as a reply-to, and send him a copy
print MAIL "Reply-to: $form{'e_mail_address'}\n";
print MAIL "Cc: $form{'e_mail_address'}\n";

# Print subject line
print MAIL "Subject: Request for more information\n";

# Terminate mail headers.
print MAIL "\n";

# Create the document body
print MAIL $form{'prefix'}." ".$form{'name'}."\n";
print MAIL "Company: ".$form{'company'}."\n";
print MAIL "Address: ".$form{'address'}."\n";
print MAIL "         ".$form{'city'}."  ".$form{'state'};
print MAIL "  ".$form{'zipcode'}."\n";
print MAIL "Phone: ".$form{'phone'}."\n";
print MAIL "Fax: ".$form{'fax'}."\n";
print MAIL "E-Mail: ".$form{'email'}."\n";
print MAIL "Comments: ".$form{'comments'}."\n";

# Close the command, and send the mail.
close (MAIL);

# Now print out a success story, so the user knows it was sent
print "<HTML>\n";
print "  <HEAD>\n";
print "    <TITLE>Thanks for Your Comments\!</TITLE>\n";
print "  </HEAD>\n";
print "  <BODY BGCOLOR=\"FFFFFF\">\n";
print "    <H2 ALIGN=\"center\">Thanks for Your Comments\!</H2>\n";
print "    <HR SIZE=5>\n";
print "    <P>\n";
print "Thank you taking the time to submit your comments.  We will ";
print "take them under advisement.\n";
print "    <P>\n";
print "    <HR SIZE=5>\n";
print "    <CENTER>\n";
print "      <A HREF=\"index.html\">Home</A>\n";
print "      <P>\n";
print "      <HR>\n";
print "    </CENTER>\n";
print "  </BODY>\n";
print "</HTML>\n";

exit(0);
