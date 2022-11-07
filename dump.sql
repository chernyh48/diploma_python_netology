--
-- PostgreSQL database dump
--

-- Dumped from database version 14.5
-- Dumped by pg_dump version 14.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

ALTER TABLE ONLY public.result DROP CONSTRAINT result_pkey;
ALTER TABLE public.result ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.result_id_seq;
DROP TABLE public.result;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: result; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.result (
    id integer NOT NULL,
    id_user integer NOT NULL,
    id_profile integer NOT NULL
);


ALTER TABLE public.result OWNER TO postgres;

--
-- Name: result_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.result_id_seq OWNER TO postgres;

--
-- Name: result_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.result_id_seq OWNED BY public.result.id;


--
-- Name: result id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.result ALTER COLUMN id SET DEFAULT nextval('public.result_id_seq'::regclass);


--
-- Data for Name: result; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.result (id, id_user, id_profile) VALUES (1, 174366164, 669829030);
INSERT INTO public.result (id, id_user, id_profile) VALUES (2, 67420444, 498817667);
INSERT INTO public.result (id, id_user, id_profile) VALUES (3, 67420444, 362941216);
INSERT INTO public.result (id, id_user, id_profile) VALUES (4, 174366164, 542639610);
INSERT INTO public.result (id, id_user, id_profile) VALUES (5, 174366164, 572417773);


--
-- Name: result_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.result_id_seq', 5, true);


--
-- Name: result result_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.result
    ADD CONSTRAINT result_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

