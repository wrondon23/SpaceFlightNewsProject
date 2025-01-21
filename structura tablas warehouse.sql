

CREATE TABLE IF NOT EXISTS public.dim_news_source (
    source_id INT IDENTITY(1, 1) PRIMARY KEY, -- Campo autoincremental para la clave primaria
    id int,                                    -- ID de la fuente
    name VARCHAR(600) NOT NULL,              -- Nombre de la fuente
    url VARCHAR(6000),                       -- URL de la fuente
    category VARCHAR(100)                    -- Categoría de la fuente
)
DISTSTYLE KEY                               -- Define el estilo de distribución
DISTKEY (id);                               -- Campo de distribución basado en el ID de la fuente


CREATE TABLE IF NOT EXISTS public.dim_topic (
    topic_id INT IDENTITY(1, 1) PRIMARY KEY, -- Campo autoincremental para la clave primaria
    id int ,                -- ID del tema
    name VARCHAR(6000) NOT NULL,             -- Nombre del tema
    category VARCHAR(6000)                   -- Categoría del tema
)
DISTSTYLE KEY                              -- Define el estilo de distribución
DISTKEY (id);                              -- Campo de distribución basado en el ID del tema



CREATE TABLE IF NOT EXISTS public.fact_article (
    article_id INT IDENTITY(1, 1) PRIMARY KEY,  -- Identificador único del artículo
    source_id INT NOT NULL,                     -- Clave foránea a la dimensión dim_news_source
    topic_id INT NOT NULL,                      -- Clave foránea a la dimensión dim_topic
    published_at TIMESTAMP NOT NULL,            -- Fecha y hora de publicación del artículo
    sentiment_score int                -- Puntuación de sentimiento del artículo
)
DISTSTYLE KEY                                   -- Estilo de distribución por clave
DISTKEY (article_id)                           -- Clave de distribución basada en article_id
SORTKEY (published_at);                        -- Clave de ordenación basada en la fecha de publicación