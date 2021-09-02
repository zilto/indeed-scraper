import scraper
import job_model
import config

DBNAME = config.DBNAME

def main():
    session = job_model.initialize(DBNAME)
    job_entries = scraper.get_all_pages(job_name="dentiste", location="Montreal")
    print(type(job_entries), len(job_entries))
    job_model.write_to_db(session, job_entries)
    job_model.read_db(session)


if __name__ == "__main__":
    main()
