#!/usr/bin/perl

$output = "";
$output2 = "";
$flag = -1;

#arg[0] = python output; arg[1] = excel output\n

$python = `cat $ENV{PWD}/$ARGV[0]`;
$excel = `cat $ENV{PWD}/$ARGV[1]`;

#below deals with the case buy, undefined, underfined, buy
#excel will give buy, buy...
#this will filter it to buy 
@lines = split("\r", $excel);
foreach $line (@lines) {
    $line = `echo $line | cut -d',' -f1,2,9,18`; 
    if ( $line =~ /l$/ && $flag != 1) {
        $excelOutput .= $line;
        $flag = 1;
    } elsif ( $line =~ /y$/ && $flag != 0) {
        $excelOutput .= $line;
        $flag = 0;
    }
   
}

#simply putting csv into a variable so I can print it
@lines = split("\n", $python);
$i = 0;
foreach $line (@lines) {
    $line = `echo $line | cut -d',' -f1,2,3,6`; 
    if($i > 0){
        $pythonOutput .= $line;
    }    
    $i += 1;
}


my $filename = 'excelOutput.txt';
open(my $fh, '>', $filename) or die "Could not open file '$filename' $!";
print $fh "$excelOutput";
close $fh;
my $filename2 = 'pythonOutput.txt';
open(my $fh2, '>', $filename2) or die "Could not open file '$filename' $!";
print $fh2 "$pythonOutput";
close $fh2;

#print $excelOutput;
#print "----------------------\n";
#print $pythonOutput;
#print "----------------------\n";

$diff = `diff -iwy $filename $filename2`;
print $diff;


