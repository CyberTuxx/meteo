-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Hôte : localhost
-- Généré le :  mar. 19 déc. 2017 à 19:34
-- Version du serveur :  10.1.26-MariaDB
-- Version de PHP :  7.0.23

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `phpmyadmin`
--

-- --------------------------------------------------------

--
-- Structure de la table `Meteo`
--

CREATE TABLE `Meteo` (
  `temp` int(11) NOT NULL,
  `pression` int(11) NOT NULL,
  `humidity` int(11) NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Déchargement des données de la table `Meteo`
--

INSERT INTO `Meteo` (`temp`, `pression`, `humidity`, `date`) VALUES
(34, 547, 14, '2017-12-19 14:37:16'),
(40, 1012, 44, '2017-12-19 15:15:43'),
(18, 741, 66, '2017-12-19 15:16:06'),
(22, 450, 44, '2017-12-19 15:16:10'),
(29, 950, 37, '2017-12-19 15:16:14'),
(-18, 390, 8, '2017-12-19 17:16:58'),
(5, 648, 48, '2017-12-19 17:17:38'),
(10, 1085, 24, '2017-12-21 11:25:58');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `Meteo`
--
ALTER TABLE `Meteo`
  ADD PRIMARY KEY (`date`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
