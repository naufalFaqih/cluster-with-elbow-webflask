-- ============================================================
-- Schema MySQL — Pemetaan Ketimpangan Digital Jawa Barat
-- ============================================================

-- 5.1 users
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 5.2 wilayah
CREATE TABLE IF NOT EXISTS wilayah (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_wilayah VARCHAR(100) NOT NULL,
    provinsi VARCHAR(100) DEFAULT 'Jawa Barat',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 5.3 data_ketimpangan
CREATE TABLE IF NOT EXISTS data_ketimpangan (
    id INT AUTO_INCREMENT PRIMARY KEY,
    wilayah_id INT NOT NULL,
    tahun INT NOT NULL,
    internet FLOAT NOT NULL,
    laptop FLOAT NOT NULL,
    smartphone FLOAT NOT NULL,
    literasi_digital FLOAT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (wilayah_id) REFERENCES wilayah(id) ON DELETE CASCADE
);

-- 5.4 hasil_clustering
CREATE TABLE IF NOT EXISTS hasil_clustering (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_ketimpangan_id INT NOT NULL,
    cluster INT NOT NULL,
    kategori VARCHAR(50) NOT NULL,
    internet_norm FLOAT,
    laptop_norm FLOAT,
    smartphone_norm FLOAT,
    literasi_digital_norm FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (data_ketimpangan_id) REFERENCES data_ketimpangan(id) ON DELETE CASCADE
);

-- 5.5 evaluasi_clustering
CREATE TABLE IF NOT EXISTS evaluasi_clustering (
    id INT AUTO_INCREMENT PRIMARY KEY,
    jumlah_cluster INT NOT NULL,
    sse FLOAT,
    silhouette_score FLOAT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
