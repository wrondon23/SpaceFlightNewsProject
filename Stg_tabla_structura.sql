CREATE TABLE stg.tbl_spaceflight_data (
    id integer ENCODE az64,
    image_url character varying(6000) ENCODE lzo,
    news_site character varying(6000) ENCODE lzo,
    published_at timestamp without time zone ENCODE az64,
    summary character varying(6000) ENCODE lzo,
    title character varying(6000) ENCODE lzo,
    updated_at timestamp without time zone ENCODE az64,
    url character varying(6000) ENCODE lzo,
    keywords character varying(6000) ENCODE lzo,
    sentiment_score integer ENCODE az64,
    classification character varying(400) ENCODE lzo
) DISTSTYLE AUTO;