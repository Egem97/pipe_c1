import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from job.pipeline_ingest import pipeline_data_c1


import pytz

async def main():
    scheduler = AsyncIOScheduler(timezone=pytz.timezone('America/Lima'))
    
    # Ejecutar cada 30 minutos desde las 8:00 AM hasta las 22:30 PM (10:30 PM)
    scheduler.add_job(pipeline_data_c1, 'cron', hour='8-22', minute='0,30')
    
    
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