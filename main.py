import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from job.pipeline_ingest import pipeline_data_c1


async def main():
    scheduler = AsyncIOScheduler()
    
    #scheduler.add_job(pipeline_data_c1, 'interval', minutes=60)
    scheduler.add_job(pipeline_data_c1, 'cron', hour='19', minute=59, timezone='America/Lima')
    
    scheduler.start()
    print("Scheduler iniciado. Ejecutando jobs.")

    # Mantener el proceso vivo
    try:
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == "__main__":
    asyncio.run(main())