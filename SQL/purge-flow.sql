-- Cleaning running jobs
delete from flo_jobrun;
delete from flo_jobbasket;

-- Cleaning archives
delete from flo_FMKArchiveSuccess;
delete from flo_FMKArchiveError;
