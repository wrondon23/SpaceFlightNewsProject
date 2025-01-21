CREATE OR REPLACE PROCEDURE public.load_data_spaceWD()
LANGUAGE plpgsql
AS $$
BEGIN
    -- Borrar todos los datos de la tabla dim_news_source
    TRUNCATE TABLE public.dim_news_source;

    -- Insertar nuevos datos en la tabla dim_news_source
    INSERT INTO public.dim_news_source (id, name, url, category)
    SELECT
        id, 
        news_site AS name,
        url,
        'Agencia_Espacial' AS category
    FROM
        "warehousepaceflight"."stg"."tbl_spaceflight_data";

    COMMIT;

    -- Borrar todos los datos de la tabla dim_topic
    TRUNCATE TABLE public.dim_topic;

    -- Insertar nuevos datos en la tabla dim_topic
    INSERT INTO public.dim_topic(id, name, category)
    SELECT
        id, 
        title AS name,
        classification AS category
    FROM
        "warehousepaceflight"."stg"."tbl_spaceflight_data";

    COMMIT;

    -- Actualizar los registros existentes en la tabla fact_article
    UPDATE public.fact_article
    SET 
        sentiment_score = source.sentiment_score
    FROM (
        SELECT
            source.source_id,
            topic.topic_id,
            CD.published_at,
            CD.sentiment_score
        FROM
            "warehousepaceflight"."stg"."tbl_spaceflight_data" CD
        LEFT JOIN dim_news_source AS source
            ON source.id = CD.id
        LEFT JOIN dim_topic topic
            ON topic.id = CD.id
    ) AS source
    WHERE public.fact_article.source_id = source.source_id
        AND public.fact_article.topic_id = source.topic_id
        AND public.fact_article.published_at = source.published_at;

    COMMIT;

    -- Insertar los nuevos registros que no existen en fact_article
    INSERT INTO public.fact_article (source_id, topic_id, published_at, sentiment_score)
    SELECT
        source.source_id,
        topic.topic_id,
        CD.published_at,
        CD.sentiment_score
    FROM
        "warehousepaceflight"."stg"."tbl_spaceflight_data" CD
    LEFT JOIN dim_news_source AS source
        ON source.id = CD.id
    LEFT JOIN dim_topic topic
        ON topic.id = CD.id
    WHERE NOT EXISTS (
        SELECT 1
        FROM public.fact_article target
        WHERE target.source_id = source.source_id
        AND target.topic_id = topic.topic_id
        AND target.published_at = CD.published_at
    );

    COMMIT;
END;
$$;

