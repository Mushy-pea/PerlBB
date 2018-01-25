&main;
exit(0);

sub main {
my($user_test, %hex_hash, $n, $sample, $image_name, $page, $username);
$username = $mod_verify::username;
$user_test = "";
%hex_hash = ("0", "0", "1", "1", "2", "2", "3", "3", "4", "4", "5", "5", "6", "6", "7", "7", "8", "8", "9", "9", "10", "A", "11", "B", "12", "C", "13", "D", "14", "E", "15", "F");
$page = "<html><head><title>Image verification</title></head><body><h1>Image verification</h1><p>Please enter the sequence of characters you see in the image into the text box.  This step is to guard the forum against spam bots.  The test is not case sensitive.</p><h1>Image</h1>";
for ($n = 0; $n < 8; $n++) {
$sample = rand 16;
$sample = int $sample;
$user_test = $user_test . $hex_hash{$sample};
$image_name = "$hex_hash{$sample}tile.gif";
$page = $page . "<img src=\"$image_name\">";
}
$page = $page . "<form action=\"forum.cgi?register+1\" method=\"post\"><input type=\"text\" name=\"user_test\"><br><input type=\"hidden\" name=\"username\" value=\"$username\"><input type=\"submit\" value=\"Verify account\"></form></body></html>~$user_test";
return $page;

}

