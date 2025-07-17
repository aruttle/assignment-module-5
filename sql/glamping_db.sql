--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (Debian 16.9-1.pgdg120+1)
-- Dumped by pg_dump version 17.4

-- Started on 2025-06-07 16:53:00

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE IF EXISTS glamping_db;
--
-- TOC entry 3397 (class 1262 OID 16389)
-- Name: glamping_db; Type: DATABASE; Schema: -; Owner: glamping_db_user
--

CREATE DATABASE glamping_db WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF8';


ALTER DATABASE glamping_db OWNER TO glamping_db_user;

\connect glamping_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3398 (class 0 OID 0)
-- Name: glamping_db; Type: DATABASE PROPERTIES; Schema: -; Owner: glamping_db_user
--

ALTER DATABASE glamping_db SET "TimeZone" TO 'utc';


\connect glamping_db

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 3389 (class 0 OID 16418)
-- Dependencies: 220
-- Data for Name: accommodation; Type: TABLE DATA; Schema: public; Owner: glamping_db_user
--

INSERT INTO public.accommodation VALUES (1, 'Cozy Cabin #1', 'A warm, wooden cabin', 120, '/static/images/cabin.jpg', 1);
INSERT INTO public.accommodation VALUES (2, 'Forest Yurt', 'A spacious yurt in the forest', 150, '/static/images/yurt.jpg', 2);
INSERT INTO public.accommodation VALUES (3, 'Sky Treehouse', 'A treehouse with great views', 200, '/static/images/treehouse.jpg', 3);
INSERT INTO public.accommodation VALUES (4, 'Lakeside Cabin', 'Cabin by the lake', 130, '/static/images/gallery7.jpg', 1);
INSERT INTO public.accommodation VALUES (5, 'Cozy Cabin #2', 'A warm, wooden cabin', 120, '/static/images/gallery4.jpg', 1);
INSERT INTO public.accommodation VALUES (6, 'Shannon Treehouse', 'A Treehouse with great views of the Shannon river ', 120, '/static/images/gallery8.jpg', 3);


--
-- TOC entry 3387 (class 0 OID 16409)
-- Dependencies: 218
-- Data for Name: accommodation_type; Type: TABLE DATA; Schema: public; Owner: glamping_db_user
--

INSERT INTO public.accommodation_type VALUES (1, 'Cabin');
INSERT INTO public.accommodation_type VALUES (2, 'Yurt');
INSERT INTO public.accommodation_type VALUES (3, 'Treehouse');


--
-- TOC entry 3391 (class 0 OID 16432)
-- Dependencies: 222
-- Data for Name: booking; Type: TABLE DATA; Schema: public; Owner: glamping_db_user
--

INSERT INTO public.booking VALUES (1, 1, 1, '2025-06-25', '2025-06-26');
INSERT INTO public.booking VALUES (2, 2, 4, '2025-06-26', '2025-06-27');
INSERT INTO public.booking VALUES (3, 3, 2, '2025-06-07', '2025-06-15');
INSERT INTO public.booking VALUES (4, 4, 2, '2025-11-07', '2025-11-15');


--
-- TOC entry 3385 (class 0 OID 16400)
-- Dependencies: 216
-- Data for Name: guest; Type: TABLE DATA; Schema: public; Owner: glamping_db_user
--

INSERT INTO public.guest VALUES (1, 'Alan ', 'alan@gmail.com', '087465464654');
INSERT INTO public.guest VALUES (2, 'Lisa', 'a@gmail.com', '0876466456');
INSERT INTO public.guest VALUES (3, 'John', 'Doe@gmail.com', '00550114534');
INSERT INTO public.guest VALUES (4, 'Bruce', 'wayne@gmail.com', '555882686');


--
-- TOC entry 3404 (class 0 OID 0)
-- Dependencies: 219
-- Name: accommodation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: glamping_db_user
--

SELECT pg_catalog.setval('public.accommodation_id_seq', 1, false);


--
-- TOC entry 3405 (class 0 OID 0)
-- Dependencies: 217
-- Name: accommodation_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: glamping_db_user
--

SELECT pg_catalog.setval('public.accommodation_type_id_seq', 1, false);


--
-- TOC entry 3406 (class 0 OID 0)
-- Dependencies: 221
-- Name: booking_id_seq; Type: SEQUENCE SET; Schema: public; Owner: glamping_db_user
--

SELECT pg_catalog.setval('public.booking_id_seq', 4, true);


--
-- TOC entry 3407 (class 0 OID 0)
-- Dependencies: 215
-- Name: guest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: glamping_db_user
--

SELECT pg_catalog.setval('public.guest_id_seq', 4, true);


-- Completed on 2025-06-07 16:53:08

--
-- PostgreSQL database dump complete
--

