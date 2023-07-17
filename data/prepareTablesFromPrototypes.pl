#!/usr/bin/perl

use warnings;
use strict;

sub parseEnrichedExc($$);
sub parseEnrichedInh($$);
sub printTableEnriched($$);

sub parseExpressed($$$);
sub printTableExpressed($$$$);

sub fixBrainRegionsNaming($);


main:{
    my %table_enriched = ();
    my %table_expressed = ();
    my $file_enriched_exc = 'data/prototypes/Synapse_enriched_v3_lookup.csv';
    my $file_enriched_inh = 'data/prototypes/cort_inh_lookup_extended.csv';
    my $file_expressed_exc = 'data/prototypes/20211203_001810_Spectronaut 15 - BR3 libv2 - v10_Report.xls - v10 interact all comparisons SampleQuantification.csv';
    my $file_expressed_inh = 'data/prototypes/20211206_165624_Cortical inhibitory cleanup-free lib1 v2_paired SampleQuantification.csv';
    my $file_out_enriched = 'data/tableEnriched.csv';
    my $file_out_expressed = 'data/tableExpressed.csv';
    
    parseEnrichedExc(\%table_enriched, $file_enriched_exc);
    parseEnrichedInh(\%table_enriched, $file_enriched_inh);
    printTableEnriched(\%table_enriched, $file_out_enriched);

    my $tag_exc = "excitatory";
    my $tag_inh = "inhibitory";
    parseExpressed(\%table_expressed, $file_expressed_exc, $tag_exc);
    parseExpressed(\%table_expressed, $file_expressed_inh, $tag_inh);
    printTableExpressed(\%table_expressed, $file_out_expressed, $tag_exc, $tag_inh);
}


sub fixBrainRegionsNaming($)
{
    my $line = $_[0];
    $line =~ s/BULB|Bulb/OlfactoryBulb/g;
    $line =~ s/CX/Cortex/g;
    $line =~ s/HC/Hippocampus/g;
    $line =~ s/STR/Striatum/g;
    $line =~ s/CER/Cerebellum/g;
    $line =~ s/DAT/Dat1/g;
    return $line;
}



sub printTableExpressed($$$$)
{
    my $table = $_[0];
    my $file_out = $_[1];
    my $tag_exc = $_[2];
    my $tag_inh = $_[3];
    my $delim = ",";

    # construct header
    my @header_exc = @{$table->{"header"}{$tag_exc}};
    my $count_exc = scalar(@header_exc);
    my @header_inh = @{$table->{"header"}{$tag_inh}};
    my $count_inh = scalar(@header_inh);

    #print join("\n", @header_exc),"\n";
    #print join("\n", @header_inh),"\n";

    my @default_exc = (0) x $count_exc;
    my @default_inh = (0) x $count_inh;
    my $d = $table->{"data"};
    open(my $fo, ">", $file_out) or die $!;

    print $fo "protein", $delim, join($delim, @header_exc),$delim,join($delim, @header_inh),"\n";
    foreach my $key (sort { $d->{$a} <=> $d->{$b} } keys(%$d)) {
        print $fo $key,$delim;
        if (exists($d->{$key}{$tag_exc})) {
            print $fo join($delim, @{$d->{$key}{$tag_exc}});
        }
        else {
            print $fo join($delim, @default_exc);
        }
        print $fo $delim;
        if (exists($d->{$key}{$tag_inh})) {
            print $fo join($delim, @{$d->{$key}{$tag_inh}});
        }
        else {
            print $fo join($delim, @default_inh);
        }
        print $fo "\n";
    }
}


sub parseExpressed($$$)
{
    my $table = $_[0];
    my $file = $_[1];
    my $tag = $_[2];

    open(my $fh, "<", $file) or die $!;

    # read header
    my $line = <$fh>;
    chomp($line);
    $line =~ s/_[0-9]+//g;
    $line =~ s/\"//g;
    $line = fixBrainRegionsNaming($line);

    my @header = split(",", $line);
    splice(@header, 0, 2);

    my @colnames = ();
    foreach my $key (@header) {
        my $brain = "unknown";
        my $mouse = "unknown";
        my $tmp = "";

        if ($tag eq "excitatory") {
            ($mouse, $brain, $tmp) = split("-", $key);
            if ($brain eq "CONTROL") {
                $brain = $mouse;
                $mouse = "Unsorted";
            }
        }
        elsif($tag eq "inhibitory") {
            $key = "Unsorted" if ($key eq "P2");
            $mouse = $key;
            $brain = "CorticalInterneurons";
        }

        $mouse .= '-cre' if($mouse ne 'Unsorted');

        my $col_name = $brain . '.' . $mouse;
        push(@colnames, $col_name);
    }

    $table->{"header"}{$tag} = \@colnames;
    while(<$fh>) {
        chomp($_);
        $_ =~ s/\"//g;
        my ($idx, $protein, @values) = split(",", $_);
        for my $i (0..$#values) {
            $values[$i] = 0 if ($values[$i] eq 'NA');
        }
        $table->{"data"}{$protein}{$tag} = \@values;
    }
    close($fh);
}


sub printTableEnriched($$)
{
    my $table_enriched = $_[0];
    my $file_out = $_[1];
    my $delim = ",";
    my $h = $table_enriched->{"header"};
    my $d = $table_enriched->{"data"};
    my @colnames = sort { $h->{$a} <=> $h->{$b} } keys(%$h);
    my @rownames = sort { $d->{$a} <=> $d->{$b} } keys(%$d);
    open(my $fo, ">", $file_out) or die $!;
    print $fo "protein", $delim, join($delim, @colnames), "\n";
    foreach my $row (@rownames) {
        my @values = (0) x scalar(@colnames);
        my $idx = 0;
        foreach my $col (@colnames) {
            $values[$idx]++ if (exists($d->{$row}{$col}));
            $idx++;
        }
        print $fo $row, $delim, join($delim, @values), "\n";
    }
    close($fo);
}


sub parseEnrichedExc($$)
{
    my $table_enriched = $_[0];
    my $file_enriched = $_[1];
    open(my $fh, "<", $file_enriched) or die $!;
    while(<$fh>) {
        chomp($_);
        next if($_ =~ m/Protein/g);
        $_ =~ s/\"//g;
        $_ =~ s/ enriched//g;
        my @line = split(',', $_, 4);
        my $protein = $line[1];
        my $group = $line[3];
        $group = fixBrainRegionsNaming($group);
        $group =~ s/\_/\./g;
        $group = "Striatum.Dat1" if ($group eq "Dat1.Dat1");
        $group .= "-cre";

        $table_enriched->{"data"}{$protein}{$group}++;
        $table_enriched->{"header"}{$group}++;
    }
    close($fh);
}

sub parseEnrichedInh($$)
{
    my $table_enriched = $_[0];
    my $file_enriched = $_[1];
    open(my $fh, "<", $file_enriched) or die $!;
    while(<$fh>) {
        chomp($_);
        next if($_ =~ m/Protein/g);
        $_ =~ s/\"//g;
        my @line = split(',', $_, 34);
        my $protein = $line[1];
        my $group = $line[33];
        $group = fixBrainRegionsNaming($group);
        $group = 'CorticalInterneurons.' . $group;
        $group .= "-cre";
        $table_enriched->{"data"}{$protein}{$group}++;
        $table_enriched->{"header"}{$group}++;
    }
    close($fh);
}

#cut -f2,4 -d"," | perl -p -e "s/ enriched//g"|perl -p -e "s/\"//g"|perl -p -e "s/\_/\,/g"
#cut -f2,34 -d","  | perl -p -e "s/\"//g" | awk -F"," 'OFS=","{print $1,"INH",$2}'
