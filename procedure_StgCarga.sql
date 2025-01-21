CREATE OR REPLACE PROCEDURE stg.reload_spaceflight_data()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Borrar todos los datos de la tabla stg.tbl_spaceflight_data
    TRUNCATE TABLE warehousepaceflight.stg.tbl_spaceflight_data;

    -- Cargar nuevamente los datos en la tabla stg.tbl_spaceflight_data desde el archivo Parquet en S3
    COPY warehousepaceflight.stg.tbl_spaceflight_data
    FROM 's3://spaceflightbuckes2025/Gold/Final_Data/'
    IAM_ROLE 'arn:aws:iam::408069808361:role/service-role/AmazonRedshift-CommandsAccessRole-20250120T084728'
    FORMAT AS PARQUET;

    COMMIT;
END;
$$;