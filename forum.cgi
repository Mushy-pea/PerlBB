#!/usr/bin/perl -T
$ENV{"PATH"} = "";
delete @ENV{qw(IFS CDPATH ENV BASH_ENV)};

# PerlBB code by Steven Tinsley.
# Usage of the works is permitted provided that this instrument is retained with the works, so that any entity that uses the works is notified of this instrument.
#DISCLAIMER: THE WORKS ARE WITHOUT WARRANTY.

use strict;
use warnings;

print "Content-type: text/html\n\n";

$conf::MESSAGE_DB = "post_log.db"; $conf::MEMBER_DB = "member.db";
$conf::THREAD_ID_FILE = "thread_id.log"; $conf::LIST_FILE_POSTFIX = "forum_list.xml";
$conf::MEMBER_LOG = "member.log"; $conf::THREADS_PER_PAGE = 21; $conf::REPLIES_PER_PAGE = 10;
$conf::environment = "server";
$conf::LIST_BASENUM = 100;
$conf::NUM_LIST_FILES = 3;
$conf::LINK_DEFAULT_FILL = " ";
for ($misc::n = 0; $misc::n < 200; $misc::n++) {
$conf::LINK_DEFAULT_FILL = $conf::LINK_DEFAULT_FILL . " ";
}
@conf::user_selections = ("display_page", "enter_post", "register", "view_post", "login");
%conf::valid_args = ("display_page", 1, "enter_post", 0, "register", 0, "view_post", 1, "login", 1);
$conf::LIST_MODE = 1;
$conf::FORUM_NAME = "www.mushy-pea.org.uk";
$conf::ADMIN_EMAIL = "steven-tinsley\@mushy-pea.org.uk";
$conf::COOKIE_DURATION = 900;

&main(@conf::user_selections, %conf::valid_args);
exit(0);

sub main() {
my($given_password, $select, $flag_safe, @args, $count, @user_selections, %valid_args, $code, $n, $value, $length, $m, $ref, @passed_array);
(@passed_array) = @_;
@user_selections = splice(@passed_array, 0, 6); %valid_args = splice(@passed_array, 0);
$count = 0; $flag_safe = 0;
if ($conf::environment eq "localhost") {$main::QUERY_STRING = <STDIN>}
elsif ($conf::environment eq "server") {$main::QUERY_STRING = $ENV{'QUERY_STRING'}}
else {die("Invalid value $conf::environment for configuration variable \$conf::environment.")}
@args = split(/\+/, $main::QUERY_STRING);
foreach (@user_selections) {
unless ($main::QUERY_STRING !~ /($_)/) {
$flag_safe = 1;
$args[0] = $1;
last;
}
}

foreach (@args) {
if ($count == $valid_args{$args[0]}) {last}
elsif ($count == 0) {$count++; next}
else {
	unless ($_ =~ /([0-9]{9})/) {&security_alert("Invalid query string", 0, 1)}
$args[$count] = $1;
$count++;
}
}

foreach (@args) {
$_ =~ /([_a-z0-9]*)/;
$_ = $1;
}

$ref = \@args;
$code = "&$args[0](\$ref)";
$value = eval($code);
#print "<br>code: $code value: $value error: $@";
exit(0);
}

sub process_form {
my($field, @expected_names, @given_names, @max_length, $num_fields, $status, $m, $n, @input1, @block1, @block2, $original_field, $length, $offset1, $offset2, $count, $grab, $replace, $result, $input, $flag_done, @passed_array); $flag_done = 0; $m = 1;
($field, $num_fields, $status, @passed_array) = @_;
$input = <STDIN>;
@expected_names = splice(@passed_array, 0, 6);
@max_length = splice(@passed_array, 0);
#print "\nmax_length: @max_length"; print "\nexpected_names: @expected_names";
@block1 = split(/&/, $input, $num_fields);
for ($n = 0; $n < $num_fields; $n++)
{
unless ($block1[$n] =~ /={1}/) {&security_alert("Invalid form caught.", 2, 1)}
$block1[$n] =~ /([^=]*)([.]*)/;
if ($1 eq $expected_names[$n])
{
$given_names[$n] = $1;
$block1[$n] = reverse($block1[$n]);
$block1[$n] =~ /([^=]*)([.]*)/;
@$field[$n] = $1;
unless (length(@$field[$n]) <= $max_length[$n]) {&security_alert("Invalid form caught.", $max_length[$n], length(@$field[$n]))}
$original_field = reverse(@$field[$n]); @$field[$n] = "";
@block2 = split(/[\+]/, $original_field);
$count = 1;
foreach (@block2) {
if ($count == 1) {@$field[$n] = @$field[$n] . $_;}
else {
@$field[$n] = @$field[$n] . " " . $_;
}
$count++;
}

$original_field = @$field[$n]; @$field[$n] = "";
@block2 = split(/%/, $original_field);
$count = 1;
foreach (@block2) {
if ($count == 1) {@$field[$n] = @$field[$n] . $_;}
else {
@$field[$n] = @$field[$n] . pack("c", hex(substr($_, 0, 2))) . substr($_, 2);
}
$count++;
}

$original_field = @$field[$n]; @$field[$n] = "";
@block2 = split(/[<>]/, $original_field);
$offset1 = 0;
$count = 0;
foreach (@block2) {
$offset1 = $offset1 + length($_);
unless ($count == 0) {$offset1++}
$grab = substr($original_field, $offset1, 1);
if ($grab eq "<") {@$field[$n] = @$field[$n] . $_ . "&lt"}
elsif ($grab eq ">") {@$field[$n] = @$field[$n] . $_ . "&gt"}
else {@$field[$n] = @$field[$n] . $_}
$count++;
}

}
else {&security_alert("Invalid form caught", $expected_names[$n], $1)}
}

return 0;

}

sub display_page {
my($action, $file_num, $filename, $page, @data, $test, $whole, $header, $footer, $body, $offset1, $offset2, @date, @field, $lockfile, $output, $args);
($args) = @_; $lockfile = "lockfile2.txt";
$file_num = $args -> [1];
if ($file_num == 1800) {
&use_template(\$header, \$footer, 1, $file_num, "null");
}
elsif ($file_num == 1280) {
&use_template(\$header, \$footer, 1, $file_num, "null");
}
elsif ($file_num == 1300) {
&use_template(\$header, \$footer, 1, $file_num, "null");
}
else {
&use_template(\$header, \$footer, 0, $file_num, "null");
}
$test = chop($file_num);
$filename = $file_num . $conf::LIST_FILE_POSTFIX;
if ($test == 0) {
open(file3, "<", $filename) || die("Unable to open file $filename for reading");
@data = <file3>;
close(file3);
$body = join("", @data);
}
else {
while (-e $lockfile) {sleep 1}
open(LOCK, $lockfile);
close(LOCK);
open(file3, "+<", $filename) || die("Unable to open file $filename for read/write");
@data = <file3>;
$body = join("", @data);
$output = &update_list(0, $file_num, 0, 0, \$body, 1, @field, @date);
unless ($output eq "") {
truncate(file3, 0);
seek(file3, 0, 0);
print file3 $output;
}
$body = $body . "<div id=\"banner\" class=\"banner\"></div>";
}
close(file3);
unlink($lockfile);
$page = $header . $body . $footer;
print "\n$page";
return 0;
}

sub use_template {
my($header, $footer, $whole, $action, @data, $file_num, $file_id, $thread_id, @grab, $offset1, $flag_verify);
($header, $footer, $action, $file_num, $thread_id) = @_;
$flag_verify = 0;
open(file4, "<", "list_template.xml") || die("Unable to open list_template.xml for reading");
@data = <file4>;
close(file4);
$whole = join("", @data);
$whole =~ /<header>([^\*]*)<\*header>/;
$$header = $1;
$whole =~ /<footer>([^\*]*)<\*footer>/;
$$footer = $1;
if ($action == 0) {
chop($file_num);
$file_num++;
$file_id = $file_num . "1";
$$footer = "></div><a href=\"forum.cgi?display_page+$file_id\">Next</a>" . $$footer;
}
elsif ($action == 1) {
$flag_verify = 1;
}
elsif ($action == 2) {
$$header = $$header . "<form action=\"forum.cgi?enter_post\" method=\"post\" id=\"post\" onsubmit=\"read_cookie()\"><p>Author: <input type=\"text\" name=\"username\" id=\"username\"></p><p>Password (enter \"null\" if guest)<input type=\"password\" name=\"password\" id=\"password\"></p><p>Subject: <input type=\"text\" name=\"subject\" id=\"subject\"></p><p>Your reply: <textarea rows=\"20\" cols=\"40\" name=\"content\" id=\"content\"></textarea><input type=\"hidden\" name=\"flag_reply\" value=\"yes\" id=\"flag_reply\"><input type=\"hidden\" name=\"thread_id\" value=\"$thread_id\" id=\"thread_id\"><input type=\"submit\" value=\"Enter reply\"></form>";
$flag_verify = 1;
}
elsif ($action == 3) {
}
unless ($flag_verify == 0) {
$offset1 = index($$header, "</head>") - 1;
$grab[0] = substr($$header, 0, $offset1);
$grab[1] = substr($$header, $offset1);
$$header = $grab[0] . "<script type=\"text/javascript\" src=\"verify_user.js\"></script>" . $grab[1];
}

return 0;
}

sub view_post {
my($check, $post_id, @result, $page, $header, $footer, @middle, $middle_big, @data, $action, @result_all, $offset1, $offset2, $num_links, $chunk, $flag_done, @link, $n, $index, $test, $flag_extend, @field_name, @name_length, $dbase, $primary_key, $args, $dummy);
($args) = @_;
$post_id = $args -> [1];
@field_name = ("<subject>", "<author>", "<date+time>", "<content>", "<links>", "<post_id>"); @name_length = (9, 8, 11, 9, 7, 9); $num_links = 0; $flag_extend = 0;
&use_template(\$header, \$footer, 2, $dummy, $post_id);
&retrieve_post($post_id, \@result, \$dbase, 1, $conf::MESSAGE_DB, 5, $primary_key, @field_name, @name_length);
&escape(1, 4, \@result);
@link = split(/,/, $result[4]);
	if ($link[0] ne $conf::LINK_DEFAULT_FILL) {
$chunk = pop(@link);
		unless ($chunk ne "+") {$flag_extend = 1;}
push(@link, $chunk);
&collect_links(\@result_all, @link, $flag_extend);
$middle[0] = "<h1>Subject: $result[0]</h1><h1>Author: $result[1]</h1><h2>Date / time: $result[2]</h2><p>$result[3]</p>";
for ($n = 1; $n < ($link[0] + 1); $n++)
{
$index = ($n - 1) * 4;
$middle[$n] = "<h1>Subject: $result_all[$index]</h1><h1>Author: $result_all[$index + 1]</h1><h2>Date / time: $result[$index + 2]</h2><p>$result_all[$index + 3]</p>";
}
$middle_big = join("", @middle);
$page = $header . $middle_big . $footer;
print $page;
exit(0);
}
else
{
$middle[0] = "<h1>Subject: $result[0]</h1><h1>Author: $result[1]</h1><h2>Date / time: $result[2]</h2><p>$result[3]</p>";
$page = $header . $middle[0] . $footer;
print $page;
}

}

sub retrieve_post {
my($post_id, $quoted_length, @data, $dbase, $chunk, $chunk2, $offset1, $offset2, $offset3, $offset4, $check, $actual_length, $compare_id, $field_length, $result,  $n, $num_records, $record_frame, $flag1, $check_char, $dbase_length, $this_offset, $action, $db_file, @field_name, @name_length, $num_fields, $primary_key, @passed_array);
($post_id, $result, $dbase, $action, $db_file, $num_fields, $primary_key, @passed_array) = @_;
@field_name = splice(@passed_array, 0, 6);
@name_length = splice(@passed_array, 0);
$check_char = "null";
$num_records = 0; $flag1 = 0; $dbase_length = 0;
unless ($action != 1) {
open(file4, "<", $db_file) || die("Unable to open $db_file for reading");
@data = <file4>;
close(file4);
$$dbase = join("", @data);
}
$offset1 = index($$dbase, "<database records=") + 18;
$offset2 = index($$dbase, " ", $offset1);
$field_length = $offset2 - $offset1;
$chunk = substr($$dbase, $offset1, $field_length);
$num_records = $chunk;
$offset2 = index($$dbase, ">", $offset2) + 1;
$record_frame = $offset2 + 8;
for ($n = 0; $n < $num_records; $n++)
{
$offset1 = $record_frame;
$check = substr($$dbase, $offset1, 8);
if (1 == 1)
{
$offset2 = index($$dbase, "</record>", $offset1) + 9;
$actual_length = $offset2 - $offset1;
$offset3 = index($$dbase, "<record length>", $offset1) + 15;
$quoted_length = substr($$dbase, $offset3, 4);
	if (1 == 1)
	{
&read_fields($offset1, $offset2, $result, $dbase, 1, $n, 0, $primary_key, @field_name, @name_length);
		if (@$result[0] eq $post_id) {
$this_offset = &read_fields($offset1, $offset2, $result, $dbase, $num_fields, $n, 1, $primary_key, @field_name, @name_length);
return $this_offset;
}
		else {$record_frame = $record_frame + $actual_length;}
}
	else {
print"A database error 2 has been found. Quoted length = $quoted_length, actual length = $actual_length, record = $n.";
}
}
else {print "A database error 1 has been found.";}
}
print "<br><br><br><br>The selected record could not be found.";
return 0;
}

sub read_fields {
my($offset1, $offset2, $offset3, $offset4, $this_offset, $result, $n, $dbase, $data, @field_name, @name_length, $num_fields, $m, $check, $check2, $primary_key, $action, @passed_array);
($offset1, $offset2, $result, $dbase, $num_fields, $m, $action, $primary_key, @passed_array) = @_;
@field_name = splice(@passed_array, 0, 6); @name_length = splice(@passed_array, 0);
unless ($action == 1) {
$field_name[0] = $field_name[5];
$name_length[0] = $name_length[5];
}
for ($n = 0; $n < $num_fields; $n++)
{
$field_name[$n + 6] = "</" . substr($field_name[$n], 1);
$offset3 = index($$dbase, $field_name[$n], $offset1) + $name_length[$n];
$offset4 = index($$dbase, $field_name[$n + 6], $offset3) - 1;
unless ($n != 4) {$this_offset = $offset3}
@$result[$n] = substr($$dbase, $offset3, $offset4 - $offset3 + 1);
}
return $this_offset;

}

sub enter_post {
my(@field, $input, $offset1, $offset2, $n, $name, $field_length, $flag_guest, $flag_verify, @data, $lockfile, $output, $write_length, $write_length2, $post_id, $post_num, $dbase, $chunk, $chunk2, $num_links, $link, $num_replies, $offset_last, $result_all, @stat, $time, $check, $link_check, @offset_ext, $flag_reply, $num_records, @expected_names, @max_length, @link_info, $dummy); @expected_names = ("username", "password", "subject", "content", "flag_reply", "thread_id"); @max_length = (12, 32, 48, 8000, 3, 10);
$offset1 = 0; $post_num = 0; $chunk = ""; print "\nenter_post()";
&process_form(\@field, 6, 1, @expected_names, @max_length);
while (1) {
if ($field[4] eq "no" && $field[5] eq "null") {last}
elsif ($field[4] eq "yes" && $field[5] ne "null") {last}
else {&security_alert("Form field conflict", $field[4], $field[5])}
}
my(@user_profile);
if ($field[1] eq "null") {$flag_verify = 1;}
else
{
$flag_verify = &verify_user(@field, 0, \@user_profile);
}
&escape(0, 6, \@field);
@stat = stat($conf::MESSAGE_DB);
$lockfile = "lockfile1.txt";
while (-e $lockfile) {sleep 1;}
open(LOCK, $lockfile);
close(LOCK);
open(file8, "+<", $conf::MESSAGE_DB) || die("Unable to open $conf::MESSAGE_DB for writing.  $!");
@data = <file8>;
$dbase = join("", @data);
if ($field[4] eq "yes")
{
$flag_reply = 1;
@link_info = &update_links(\$dbase, $link, $field[5], @stat);
}
elsif ($field[4] eq "no") {$field[5] = &new_thread; $flag_reply = 0;}
else {&security_alert("Invalid form value.", 3, 0)}
unless ($flag_verify == 1) {&security_alert("User privalidges violation.", 4, 0)}
$time = time;
unless ($flag_reply == 1) {$chunk = "<links>$conf::LINK_DEFAULT_FILL</links>";}
unless ($field[1] ne "null") {
$field[0] = "Guest: $field[0]";
}
$output = "<record><record length>####</record length>$chunk<post_id>$field[5]</post_id><subject>$field[2]</subject><author>$field[0]</author><date+time>$time</date+time><content>$field[3]</content></record></database>";
$write_length = length($output);
$output =~ s/\#\#\#\#/$write_length/;
$write_length2 = length($output);
unless ($write_length == $write_length2) {
$output =~ s/[0-9]{$write_length2}/$write_length2/;
}
$dbase =~ /<database records=([0-9]*)/;
$offset1 = index($dbase, "<database records=") + 18;
$num_records = $1 + 1;
seek(file8, $offset1, 0);
print file8 $num_records;
$offset_last = $stat[7] - 11;
truncate(file8, $offset_last);
seek(file8, $offset_last, 0);
print file8 $output;
unless ($flag_reply == 0)
{
$offset1 = rindex($dbase, "<links>", $link_info[1]) + 7;
$link_info[1] = $offset1;
seek(file8, $link_info[1], 0);
print file8 $link_info[0];
}
close(file8);
unlink($lockfile);
$main::QUERY_STRING = "view_post=$field[5]";
&update_list(1, $conf::LIST_BASENUM, $flag_reply, $field[5], \$dummy, 1, $time, @field);
sleep 1;
my(@args);
$args[1] = 1600;
&display_page(\@args);
}

sub verify_user {
my(@field, $user_profile, @data, @result, @field_name, @name_length, @length, $dbase, $lockfile, $this_offset, $offset1, $offset2, $action, $grab, $args);
(@field, $action, $user_profile) = @_;
@field_name = ("<password>", "<post_count>", "<user_title>", "<user_level>", "<locate>", "<username>");
@name_length = (10, 12, 12, 12, 0, 10);
$lockfile = "lockfile10.txt";
while (-e $lockfile) {sleep 1}
open(LOCK, $lockfile);
close(LOCK);
open(file1, "+<", $conf::MEMBER_DB);
@data = <file1>;
$dbase = join("", @data);
$this_offset = &retrieve_post($field[0], \@result, \$dbase, 0, $conf::MEMBER_DB, 5, "null", @field_name, @name_length);
unless ($this_offset != 0) {return 0}
unless ($result[0] eq $field[1]) {return 0}
@{$user_profile} = ($result[1], $result[2], $result[3]);
unless ($action == 0) {
	unless (@$user_profile[2] == 1) {&security_alert("User privalidges violation", 0, 0)}
}
@$user_profile[0]++;
$offset1 = rindex($dbase, "<record>", $this_offset);
$offset2 = index($dbase, "</record>", $this_offset) + 8;
$grab = substr($dbase, $offset1, $offset2 - $offset1);
$length[0] = length($grab);
$grab =~ s/<post_count>[0-9]*/<post_count>@$user_profile[0]/;
$length[1] = length($grab);
my($replace);
if ($length[0] == $length[1]) {
seek(file1, $offset1, 0);
print file1 $grab;
}
else {
$replace = substr($dbase, $offset2 + 1);
truncate(file1, $offset1);
seek(file1, $offset1, 0);
print file1 $grab;
print file1 $replace;
}
close(file1);
unlink($lockfile);
return 1;

}

sub login {
my(@field, @expected_names, @max_length, @field_name, @name_length, @result, $this_offset, $dummy, $expire, @date, %week_day, %month, $args, $javascript, $n);
($args) = @_;
if ($args -> [1] == 1) {
%week_day = ("0", "Mon", "1", "Tue", "2", "Wed", "3", "Thu", "4", "Fri", "5", "Sat", "6", "Sun");
%month = ("0", "Jan", "1", "Feb", "2", "Mar", "3", "Apr", "4", "May", "5", "Jun", "6", "Jul", "7", "Aug", "8", "Sep", "9", "Oct", "10", "Nov", "11", "Dec");
@expected_names = ("username", "password", "cookie", "null", "null", "null");
@max_length = (12, 32, 3, 0, 0, 0);
@field_name = ("<password>", "null", "null", "null", "null", "<username>");
@name_length = (10, 0, 0, 0, 0, 10);
&process_form(\@field, 3, 0, @expected_names, @max_length);
$this_offset = &retrieve_post($field[0], \@result, $dummy, 1, $conf::MEMBER_DB, 1, "<username>", @field_name, @name_length);
unless ($result[0] eq $field[1]) {&security_alert("Invalid username and password combination supplied.", 0, 0)}
$javascript = "function cookie() {\nvar user_data = document.cookie;\n if (user_data) {\ndocument.cookie='user_data=null; expires=01 Jan 1970 00:00:01 GMT; path=/';\n}\n var date = new Date();\n date.setTime(date.getTime()+900000);\n var expires = date.toGMTString();\n document.cookie='user_data=$field[0]~$field[1]; expires=' + expires + '; path=/';\n setTimeout(\"redirect()\", 3000);\n}\n\nfunction redirect() {\nwindow.location=\"http://www.mushy-pea.org.uk/forum.cgi?display_page+1001\";\n}";
if ($field[2] eq "on") {
print "<html><head><title>Logged in</title><script type=\"text/javascript\">$javascript</script></head><body onload=\"cookie()\"><h1>Thank you for logging in $field[0]</h1><p>Click the link below if your browser doesn't redirect you.</p><a href=\"forum.cgi?display_page+1001\">Back to forum index</a></body></html>";
}
else {
print "<html><head><title>Logged in</title></head><body><h1>Your account is active, but you need to choose \"Save a cookie\" on the proceeding form to log in properly</h1><a href=\"http://$conf::FORUM_NAME/forum.cgi?display_page+1001\">Click here to return to the forum index</a></body></html>";
}
}
else {
print "<html><head><title>Logged out</title></head><body><script language=\"javascript\" type=\"text/javascript\">eraseCookie('user_info');</script><h1>You are now logged out (all cookies cleared)</h1><a href=\"forum.cgi?display_page+1001\">Back to forum index</a></body></html>";
}

}

sub update_links {
my($dbase, $n, $offset1, $offset2, $flag_done, $link, $index, $chunk, $chunk2, $offset_last, @field, @result, @block, $flag_extend, $replace, @field_name, @name_length, @stat, @link_info, $this_offset, $thread_id); $index = 0;
($dbase, $link, $thread_id, @stat) = @_;
my $size = length $$dbase;
$offset1 = 0; $offset_last = $stat[7] - 11; $flag_extend = 0;
@field_name = ("<subject>", "<author>", "<date+time>", "<content>", "<links>", "<post_id>"); @name_length = (9, 8, 11, 9, 7, 9);
$test::flag = 1;
$this_offset = &retrieve_post($thread_id, \@result, $dbase, 0, $conf::MESSAGE_DB, 5, "<post_id>", @field_name, @name_length) + 32;
unless ($this_offset != 0) {&security_alert("Primary record not found", 0, 0);}
if (chop($result[4]) eq "+") {
$offset1 = index($dbase, "</database>") + 11;
$chunk = substr($dbase, $offset1);
$chunk =~ /links id=\$field[5]>([0-9, ]*)/;
$chunk2 = $1 . ", $offset_last";
$chunk =~ s/links id=\$field[5]>[0-9, ]*/links id=\$field[5]>\$chunk2/;
$dbase =~ s/<\/database>[.]*/<\/database>\$chunk/;
$flag_extend = 1;
}
elsif (chop($result[4]) ne "+" && length($result[4]) < 986) {
$result[4] =~ /([0-9,]*)/;
$result[4] = $1 . ",$offset_last";
}
else {
$result[4] = $result[4] . "+";
$dbase = $dbase . "<links id=$field[5]>$offset_last</links>";
$flag_extend = 1;
}
@block = split(/,/, $result[4], 2);
unless ($block[0] < 9999) {&security_alert("Corrupted link field", 1, 1)}
$block[0]++;
$result[4] =~ s/[0-9]*/$block[0]/;
@link_info = ($result[4], $this_offset);
return @link_info;
}

sub collect_links {
my(@result, @data, $dbase, @link, $offset1, $offset2, $offset3, $offset4, $n, $m, $result_all, $index, $flag_extend, @field_name, @name_length);
($result_all, @link, $flag_extend) = @_; @field_name = ("<subject>", "<author>", "<date+time>", "<content>", "null", "null"); @name_length = (9, 8, 11, 9, 0, 0);
#print "<br>collect_links";
open(file9, "<", $conf::MESSAGE_DB) || die("Unable to open $conf::MESSAGE_DB for reading.  $!");
@data = <file9>;
close(file9);
$dbase = join("", @data);
unless ($flag_extend == 0) {$link[0]--;}
for ($n = 1; $n < ($link[0] + 1); $n++) {
&read_fields($link[$n], 0, \@result, \$dbase, 4, 0, 1, "<post_id>", @field_name, @name_length);
for ($m = 0; $m < 4; $m++) {
$index = ($n * 4) + $m - 4;
$result_all -> [$index] = $result[$m];
}
}

}

sub update_list {
my(@data, $body, $header, $footer, $whole, $file_num, $lockfile, $flag_reply, $output, $offset1, $offset2, $chunk, $list_entry, @field, $time, $n, $m, $post_id, $flag_done, @result, $list_page, $n_list_page, $list_header, @div_block, $filename, $count, $size, $vert_pos, $pass_down, $post_num, $action, $page, @passed_array, %id_hash, %temp_id, $top, $id, $temp, $flag_update, $length, $recurse);
($action, $file_num, $flag_reply, $post_id, $body, $recurse, $time, @field) = @_; $lockfile = "lockfile2.txt"; $flag_done = 0; $offset1 = 0; $offset2 = 0; $filename = $file_num . $conf::LIST_FILE_POSTFIX; $count = 0;
unless (($conf::LIST_MODE && $flag_reply) == 0) {return 0}
unless ($action == 0) {
while (-e $lockfile) {sleep 1;}
open(LOCK, $lockfile);
close(LOCK);
open(file11, "+<", $filename) || die("Unable to open file $filename for read/write");
@data = <file11>;
$list_page = join("", @data);
$body = \$list_page;
}
$chunk = $$body;
$count = 0;
while (1) {
if ($count == 0 && $action == 0) {
$offset1 = index($chunk, "<pos  id=");
}
else {
$offset1 = index($chunk, "<post id=");
}
if ($offset1 == -1) {last}
else {
$chunk = substr($chunk, $offset1);
$chunk =~ /<post id=([0-9]*)/;
$chunk =~ /<pos  id=([0-9]*)/;
$id = $1;
$chunk =~ /top: ([0-9]*)/;
$top = $1;
$id_hash{$top} = $id;
$chunk = substr($chunk, 9);
}
$count++;
}
@div_block = split(/<post id=[0-9]*>/, $$body);
$count = 0;
foreach (@div_block) {
if ($count == 0 && $action == 0) {
$_ =~ s/<pos  id=/<post id=/;
$_ =~ s/<\/pos >/<\/post>/;
}
else {
$_ = substr($_, 0, -7);
}
$count++;
}
unless ($action == 1) {
$div_block[0] =~ /update=([YESNO&]{3})/;
while (1) {
if ($1 eq "YES") {
$flag_update = 1;
$div_block[0] =~ /content=([^\*]*)/;
push(@div_block, $1);
last;
}
elsif ($1 eq "NO&") {
$flag_update = 0;
last;
}
else {die("The list file $filename has a corrupted header.")}
}
@div_block = splice(@div_block, 1);
}
%temp_id = %id_hash;
if ($flag_reply == 0 && $action == 1)
{
push(@div_block, "<div id=\"post$post_id\" style=\"top: 180px\" class=\"block0\"><p><strong>$field[2]</strong></p><div id=\"post$post_id\" class=\"block1\"><p><strong>$field[0], time: $time</strong></p></div><div id=\"post$post_id\" class=\"block2\"><a href=\"forum.cgi?view_post+$post_id\" onMouseOver=\"MM_swapImage('view_post1', '', 'view_post2.gif', 1)\" onMouseOut=\"MM_swapImgRestore()\"><img src=\"view_post.gif\" name=\"view_post1\"></a></div></div>");
}
elsif ($flag_reply == 1 && $action == 1)
{
foreach (@div_block) {
$_ =~ /top: ([0-9]*)/;
if ($id_hash{$1} eq $post_id) {
$_ =~ s/top: [0-9]*/top: 180/;
last;
}
else {next}
}
}
elsif ($action == 0) {
$chunk = pop(@div_block);
$chunk =~ s/top: [0-9]*/top: 180/;
push(@div_block, $chunk);
}
foreach (@div_block) {
$_ =~ /top: ([0-9]*)/;
$vert_pos = $1 + 60;
$_ =~ s/top: [0-9]*/top: $vert_pos/;
}
$$body = join("", @div_block);
my(@pushdown, $overflow);
$overflow = ($conf::THREADS_PER_PAGE * 60) + 240;
if ($flag_update == 0 && $action == 0) {$output = ""}
else {
$size = scalar @div_block;
&update_id_hash(\%id_hash, \%temp_id, $post_id, $size);
$output = "update=NO&content=null*";
for ($n = 240; $n < ($size * 60) + 240; $n = $n + 60) {
foreach (@div_block) {
unless ($_ !~ /top: $n/) {
if ($n == 240 && $action == 0) {
$output = $output . $_;
}
elsif ($n == $overflow && $action == 1) {
$_ =~ /style="([^"]*)/;
$chunk = $1;
$chunk = $chunk . "; visibility: hidden";
$_ =~ s/style="[^"]*/style="$chunk/;
$output = $output . "~<post id=$id_hash{$n}>$_</post>~";
}
else {
$output = $output . "<post id=$id_hash{$n}>$_</post>";
}

}
}
}

}

unless ($action == 0) {
truncate(file11, 0);
seek(file11, 0, 0);
print file11 $output;
close(file11);
unlink($lockfile);
}

unless ($size <= $conf::THREADS_PER_PAGE + 2 || $recurse == 0) {
@pushdown = split(/~/, $output, 3);
$pushdown[1] =~ /style="top: ([0-9]*)/;
$chunk = $1 . "px";
$pushdown[1] =~ s/style="[^"]*/style="top: $chunk/;
&list_cascade($file_num, $pushdown[1]);
}

my($code);
unless (scalar @div_block < $conf::THREADS_PER_PAGE + 5) {
my($result);
open(file30, "<", "fix_list.pl") || die("Unable to open file fix_list.pl for reading.");
@data = <file30>;
close(file30);
$code = join("", @data);
$code = "&fix_list(\$filename); " . $code;
$code =~ /([^`]*)/;
$code = $1;
$result = eval($code);
unless (defined($result) == 1) {
die("fix_list.pl failed because: $@");
}

}

return $output;

}

sub update_id_hash {
my($id_hash, $temp_id, $post_id, $n, $size, $limit);
($id_hash, $temp_id, $post_id, $size) = @_;
$limit = ($size * 60) + 240;
$id_hash -> {240} = $post_id;
for ($n = 300; $n < $limit; $n = $n + 60) {
$id_hash -> {$n} = $temp_id -> {$n - 60};
}

}

sub list_pushdown {
my($list_page, $file_num, $filename, $lockfile, $value, @data, $pushdown, $post_id, $chunk1, $chunk2);
($file_num, $pushdown) = @_;
$lockfile = "lockfile2.txt";
$file_num++;
$filename = $file_num . $conf::LIST_FILE_POSTFIX;
unless (-e $filename) {
open(file20, ">", $filename);
print file20 "update=NO&content=null*<post id=dummy><div style=\"top: 240px; visibility: hidden\"></div></post>";
close(file20);
}
while (-e $lockfile) {sleep 1}
open(LOCK, $lockfile);
close(LOCK);
open(file20, "+<", $filename);
@data = <file20>;
$list_page = join("", @data);
$pushdown =~ s/<post id=/<pos  id=/;
$pushdown =~ s/<\/post>/<\/pos >/;
$pushdown =~ /<([^>]*)><([^>]*)>/;
$chunk1 = $1;
$chunk2 = $2;
$chunk2 = substr($chunk2, 0, -12);
$pushdown =~ s/<[^>]*><[^>]*>/<$chunk1><$chunk2>/;
$list_page =~ s/update=[YESNO&]{3}/update=YES&/;
$list_page =~ s/content=[^\*]*/content=$pushdown/;
truncate(file20, 0);
seek(file20, 0, 0);
print file20 $list_page;
close(file20);
unlink($lockfile);


}

sub new_thread {
my(@data, $log, $lockfile, $next_id, $n, $replace); $lockfile = "lockfile4.txt";
$replace = "";
while (-e $lockfile) {sleep 1}
open(LOCK, $lockfile);
close(LOCK);
open(file9, "+<", $conf::THREAD_ID_FILE);
@data = <file9>;
$log = join("", @data);
$next_id = $log + 1;
for ($n = 0; $n < (9 - length($log)); $n++) {
$replace = $replace . "0";
}
$log = $replace . $log;
truncate(file9, 0);
seek(file9, 0, 0);
print file9 $next_id;
close(file9);
unlink($lockfile);
return ($log);
}

sub register {
my(@data, $dbase, @field, @expected_names, @max_length, $lockfile, @result, $output, $flag_valid, @write_length, $chunk, $chunk2, $n, @field_name, @name_length, $user_test, $args, $username, $this_offset, $offset1, $offset2);
my($pwd_hash, @stat, $result, @page, $num_records, @code);
($args) = @_;
$lockfile = "lockfile5.txt";
@field_name = ("<user_test>", "null", "null", "null", "<locate>", "<username>"); @name_length = (11, 0, 0, 0, 8, 10);
if ($args -> [1] == 0) {
@expected_names = ("username", "password", "confirm-password", "email", "null", "null"); @max_length = (12, 32, 32, 48, 0, 0);
&process_form(\@field, 4, 2, @expected_names, @max_length);
unless ($field[1] eq $field[2]) {&registration_error("The \"password\" and \"confirm-password\" fields do not match, indicating a mistake.")}
unless (length($field[0]) > 5) {&registration_error("Invalid username supplied")}
unless (length($field[1]) > 5) {&registration_error("Invalid password supplied")}

unless (length($field[3]) > 5) {&registration_error("Invalid e-mail address supplied")}
$flag_valid = index($field[3], "@");
unless ($flag_valid != -1) {&registration_error("Invalid e-mail address supplied")}
while (-e $lockfile) {sleep 1;}
open(LOCK, $lockfile);
close(LOCK);
@stat = stat $conf::MEMBER_DB;
open(file10, "+<", "$conf::MEMBER_DB") || die("Unable to open file $conf::MEMBER_DB for read / write");
@data = <file10>;
$dbase = join("", @data);
unless (&retrieve_post($field[0], \@result, \$dbase, 0, $conf::MEMBER_DB, 3, "<username>", @field_name, @name_length) == 0) {
&registration_error("This username is already in use.  Please choose another one.");
}
$result = "";
open(file11, "<", "image_verify.pl") || die($!);
@data = <file11>;
close(file11);
$code[0] = join("", @data);
$code[0] =~ /([^`]*)/;
$code[0] = $1;
$result = eval($code[0]);
if ($result eq "") {die("image_verify.pl module failed to execute properly. Reason: $@")}
@page = split(/~/, $result, 2);
$user_test = $page[1];

$output = "<record><record length>    </record length><username>$field[0]</username><password>$field[1]</password><user_level>0</user_level><user_title>$field[4]</user_title><user_image></user_image><post_count>0</post_count><user_test>$user_test</user_test><verified>no#</verified><locate></locate></record>";
$write_length[0] = length($output);
$chunk = substr($output, 27);
$write_length[1] = length($write_length[0]);
$output = "<record><record length>";
$chunk2 = "";
for ($n = 0; $n < (4 - $write_length[1]); $n++) {
$chunk2 = $chunk2 . " ";
}
$output = $output . $chunk2 . $write_length[0] . $chunk . "</database>";

$dbase =~ /<database records=([0-9]*)/;
$num_records = $1 + 1;
$offset1 = index($dbase, "<database records=") + 18;
seek(file10, $offset1, 0);
print file10 $num_records;
truncate(file10, $stat[7] - 11);
seek(file10, $stat[7] - 11, 0);
print file10 $output;
close(file10);
unlink($lockfile);
print $page[0];

}
elsif ($args -> [1] == 1) {
@expected_names = ("user_test", "username", "null", "null", "null", "null");
@max_length = (8, 12);
&process_form(\@field, 2, 0, @expected_names, @max_length);
while (-e $lockfile) {sleep 1}
open(LOCK, $lockfile);
close(LOCK);
open(file1, "+<", $conf::MEMBER_DB);
@data = <file1>;
$dbase = join("", @data);
$this_offset = &retrieve_post($field[1], \@result, \$dbase, 0, $conf::MEMBER_DB, 5, "null", @field_name, @name_length);
unless ($result[0] eq $field[0]) {&registration_error("The image verification test failed.", 0)}
$offset1 = rindex($dbase, "<verified>", $this_offset) + 10;
seek(file1, $offset1, 0);
print file1 "yes";
close(file1);
unlink($lockfile);
$args -> [1] = "1310";
&display_page($args);
}

}

sub search {
print "Content-type: text/html\n\n<html><head><title>Function not implemented</title></head><body><h1>Function not implemented</h1><p>Sorry, this function has not been implemented yet.";
}

sub escape {
my($action, $text, $n, $offset1, @block, $count, $grab, $original_text, %replace, $num_fields);
($action, $num_fields, $text) = @_;
%replace = ("%", "%0", "*", "%1", "~", "%2", "\n", "<br>");
unless ($action == 0) {%replace = reverse %replace}
for ($n = 0; $n < $num_fields; $n++) {
$original_text = @$text[$n]; @$text[$n] = "";
if ($action == 0) {@block = split(/[~%\*]/, $original_text)}
else {@block = split(/%[0-9]{1}/, $original_text)}
$offset1 = 0;
$count = 0;
foreach (@block) {
$offset1 = $offset1 + length($_);
if ($count != 0 && $action == 0) {$offset1++}
elsif ($count != 0 && $action == 1) {$offset1 = $offset1 + 2}
unless (scalar @block != 1) {@$text[$n] = $_; last}
if ($action == 0) {$grab = substr($original_text, $offset1, 1)}
else {
$grab = substr($original_text, $offset1 + 1, 1);
$grab = "%" . $grab;
}
@$text[$n] = @$text[$n] . $_ . $replace{$grab};
$count++;
}

}

}

sub list_cascade {
my($file_num, $filename, $pushdown, $n, $this_file, $list_page, $lockfile, @dummy, @data, $output);
($file_num, $pushdown) = @_;
$lockfile = "lockfile9.txt";
&list_pushdown($file_num, $pushdown);
for ($n = 1; $n < $conf::NUM_LIST_FILES; $n++) {
$this_file = $file_num + $n;
$filename = $this_file . $conf::LIST_FILE_POSTFIX;
if (-e $filename) {
while (-e $lockfile) {sleep 1}
open(LOCK, $lockfile);
close(LOCK);
open(file21, "+<", $filename);
@data = <file21>;
$list_page = join("", @data);
$output = &update_list(0, $this_file, 0, 0, \$list_page, 0, @dummy, @dummy);
unless ($output eq "") {
truncate(file21, 0);
seek(file21, 0, 0);
print file21 $output;
}
close(file21);
unlink($lockfile);

}
else {last}

}

}

sub registration_error {
my($error, $action);
($error, $action) = @_;
print "<html><head><title>Registration error</title></head><body><h1>Registration error</h1><p>It seems an error occured while processing your registration details.  The error detected was: $error.  Click back on your browser to return to the registration page and correct this mistake, or click the link below to go to the forum index.</p><a href=\"forum.cgi?display_page+1001\">Back to forum index</a></body></html>";
if ($action == 0) {exit(0)}
else {return 0}

}

sub convert_date {
my($time, $zone, @date, $date_string, @week_day);
($time, $zone) = @_;
@week_day = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday");
$time = $time + $zone * 3600;
@date = gmtime($time);
$date[4]++;
$date[5] = $date[5] + 1900;
$date_string = "on $week_day[$date[6]] $date[3]/$date[4]/$date[5] at $date[2] : $date[1]";
return $date_string;
}

sub security_alert {
my($error, $detail, $detail2); ($error, $detail, $detail2) = @_;
print "Content-type: text/html\n\n<html><head><title>Oh dear....</title></head><body><h1>Oh dear....</h1><p>Sorry, it seems a perlBB error has occured.  If you wish to submit a bug report to the developer please use perlbb\@rochfest.co.uk.</p><a href=\"forum.pl?forum_index\">Back to forum index</a></body></html>";
print "Error: $error\nDetail 1: $detail\nDetail 2: $detail2";
exit(0);
}
