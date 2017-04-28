use gp3;

# Count total N/R articles.
select count(url), tag from cklist group by tag;

# check the up-to-date list count
select count(url) from cklist where source = 'NYT' and tag = 'N' and date >= date(now());

# Get total article counts by source
select count(url), source from cklist group by source;

# Get total N/R article counts by source
select count(url), source, tag from cklist group by source, tag;