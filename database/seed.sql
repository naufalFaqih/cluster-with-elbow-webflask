-- ============================================================
-- Seed data — Pemetaan Ketimpangan Digital Jawa Barat (2023)
--   - 1 admin, 1 user (password hash pbkdf2:sha256)
--   - 27 kabupaten/kota Jawa Barat
--   - data ketimpangan 2023 (4 indikator)
--
-- Kompatibel MySQL & SQLite (INSERT OR IGNORE / INSERT IGNORE
-- diatur di kode loader; pakai INSERT polos di sini).
-- ============================================================

-- USERS ------------------------------------------------------
INSERT INTO users (nama, username, password, role) VALUES
('Administrator', 'admin', 'pbkdf2:sha256:1000000$kk8wISYg5zyXdxiR$bbfa6e3f2bb0db724e1ac666d647c64ab2f45b38fcbbf2145299374cd861dacb', 'admin');

INSERT INTO users (nama, username, password, role) VALUES
('User Demo', 'user', 'pbkdf2:sha256:1000000$xA5gzxvFVnLz5UJm$c226e520ef4aeae43a7be3c33dd4e1f0c705362d2b9e4d0945c919a64a420b06', 'user');

-- WILAYAH (27 kab/kota Jawa Barat) ----------------------------
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN BOGOR', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN SUKABUMI', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN CIANJUR', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN BANDUNG', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN GARUT', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN TASIKMALAYA', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN CIAMIS', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN KUNINGAN', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN CIREBON', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN MAJALENGKA', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN SUMEDANG', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN INDRAMAYU', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN SUBANG', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN PURWAKARTA', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN KARAWANG', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN BEKASI', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN BANDUNG BARAT', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KABUPATEN PANGANDARAN', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KOTA BOGOR', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KOTA SUKABUMI', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KOTA BANDUNG', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KOTA CIREBON', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KOTA BEKASI', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KOTA DEPOK', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KOTA CIMAHI', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KOTA TASIKMALAYA', 'Jawa Barat');
INSERT INTO wilayah (nama_wilayah, provinsi) VALUES ('KOTA BANJAR', 'Jawa Barat');

-- DATA KETIMPANGAN 2023 --------------------------------------
-- Format: (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital)
-- wilayah_id mengikuti urutan insert di atas (1..27).

INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (1,  2023, 0.9553, 0.2314, 0.3819, 0.9555);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (2,  2023, 0.9362, 0.1527, 0.5560, 0.9474);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (3,  2023, 0.9271, 0.1221, 0.2813, 0.9433);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (4,  2023, 0.9499, 0.1952, 0.5370, 0.9791);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (5,  2023, 0.9413, 0.1497, 0.4921, 0.9660);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (6,  2023, 0.9592, 0.1827, 0.5248, 0.9748);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (7,  2023, 0.9637, 0.2849, 0.6285, 0.9755);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (8,  2023, 0.9829, 0.1771, 0.5396, 0.9876);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (9,  2023, 0.9210, 0.1703, 0.5154, 0.9705);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (10, 2023, 0.9491, 0.1916, 0.5847, 0.9755);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (11, 2023, 0.9734, 0.2619, 0.6126, 0.9821);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (12, 2023, 0.9450, 0.1790, 0.7378, 0.9705);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (13, 2023, 0.9558, 0.1148, 0.4763, 0.9595);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (14, 2023, 0.9572, 0.1270, 0.5555, 0.9717);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (15, 2023, 0.9532, 0.1474, 0.4612, 0.9595);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (16, 2023, 0.9742, 0.3206, 0.3640, 0.9777);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (17, 2023, 0.9404, 0.1150, 0.5260, 0.9647);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (18, 2023, 0.9721, 0.2761, 0.4485, 0.9793);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (19, 2023, 0.9816, 0.3988, 0.5200, 0.9806);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (20, 2023, 0.9738, 0.3079, 0.8215, 0.9939);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (21, 2023, 0.9576, 0.4368, 0.7570, 0.9663);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (22, 2023, 0.9586, 0.3969, 0.8775, 0.9719);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (23, 2023, 0.9823, 0.4750, 0.5179, 0.9785);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (24, 2023, 0.9862, 0.5147, 0.7444, 0.9877);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (25, 2023, 0.9902, 0.4167, 0.5778, 0.9942);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (26, 2023, 0.9603, 0.2615, 0.7645, 0.9704);
INSERT INTO data_ketimpangan (wilayah_id, tahun, internet, laptop, smartphone, literasi_digital) VALUES (27, 2023, 0.9875, 0.2357, 0.6856, 0.9864);
