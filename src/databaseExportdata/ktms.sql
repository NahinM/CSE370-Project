-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307:3307
-- Generation Time: Sep 08, 2025 at 05:30 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ktms`
--

-- --------------------------------------------------------

--
-- Table structure for table `assets`
--

CREATE TABLE `assets` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `description` text NOT NULL,
  `siteLink` text NOT NULL,
  `contentlink` text NOT NULL,
  `createdAt` date NOT NULL,
  `updatedAt` date NOT NULL,
  `type` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `assets`
--

INSERT INTO `assets` (`id`, `title`, `description`, `siteLink`, `contentlink`, `createdAt`, `updatedAt`, `type`) VALUES
(2, 'Mountains', 'soldfghwaiulerhb', 'https://www.pexels.com/photo/brown-and-green-mountain-view-photo-842711/', 'https://images.pexels.com/photos/842711/pexels-photo-842711.jpeg', '2025-09-01', '2025-09-06', 'graphics'),
(5, 'brown and green', 'somthing somthin', 'https://www.pexels.com/photo/brown-and-green-leafed-plants-1379640/', 'https://images.pexels.com/photos/1379640/pexels-photo-1379640.jpeg', '2025-09-01', '2025-09-01', 'graphics'),
(6, 'nature sound', 'some nature sound i don\'t know', 'N/A', 'https://pixabay.com/sound-effects/007007-rainfallwav-50214/', '2025-09-06', '2025-09-06', 'audio'),
(7, 'Rain and Roads', 'something somethin', 'https://www.pexels.com/photo/black-asphalt-road-between-trees-2291430/', 'https://images.pexels.com/photos/2291430/pexels-photo-2291430.jpeg', '2025-09-06', '2025-09-06', 'graphics'),
(8, 'Dumbest Animal', 'yeaaaaaaaaaaaa', 'https://youtu.be/gtDKKJq9u30?si=7vpt87ZKfGNQJ5cf', 'https://youtu.be/gtDKKJq9u30', '2025-09-07', '2025-09-07', 'video'),
(9, 'Pixel 10/pro', 'Review of the pixel phone. the style can be used in project 11102', 'https://www.youtube.com/watch?v=i63u-iAnhuk&t=1s', 'https://youtu.be/i63u-iAnhuk', '2025-09-08', '2025-09-08', 'video');

-- --------------------------------------------------------

--
-- Table structure for table `asset_genre`
--

CREATE TABLE `asset_genre` (
  `asset_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `asset_genre`
--

INSERT INTO `asset_genre` (`asset_id`, `genre_id`) VALUES
(2, 1),
(2, 4),
(5, 1),
(2, 7),
(6, 2),
(6, 4),
(7, 9),
(8, 2),
(9, 1),
(9, 4);

-- --------------------------------------------------------

--
-- Table structure for table `asset_mainctg`
--

CREATE TABLE `asset_mainctg` (
  `asset_id` int(11) NOT NULL,
  `main_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `asset_mainctg`
--

INSERT INTO `asset_mainctg` (`asset_id`, `main_id`) VALUES
(2, 1),
(5, 1),
(6, 1),
(7, 1),
(8, 1),
(9, 1),
(9, 2);

-- --------------------------------------------------------

--
-- Table structure for table `asset_subctg`
--

CREATE TABLE `asset_subctg` (
  `asset_id` int(11) NOT NULL,
  `sub_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `asset_subctg`
--

INSERT INTO `asset_subctg` (`asset_id`, `sub_id`) VALUES
(2, 3),
(5, 2),
(5, 3),
(6, 3),
(6, 7),
(7, 3),
(8, 2),
(9, 2);

-- --------------------------------------------------------

--
-- Table structure for table `bookmark`
--

CREATE TABLE `bookmark` (
  `user_id` varchar(255) NOT NULL,
  `asset_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookmark`
--

INSERT INTO `bookmark` (`user_id`, `asset_id`) VALUES
('abc', 5),
('nahin', 8),
('nahin', 7);

-- --------------------------------------------------------

--
-- Table structure for table `genre`
--

CREATE TABLE `genre` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `genre`
--

INSERT INTO `genre` (`id`, `name`) VALUES
(1, 'aaa'),
(2, 'bbb'),
(3, 'ddd'),
(4, 'ccc'),
(5, 'www'),
(6, 'aaaa'),
(7, 'wwe'),
(8, 'ggg'),
(9, 'eee');

-- --------------------------------------------------------

--
-- Table structure for table `maincategory`
--

CREATE TABLE `maincategory` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `maincategory`
--

INSERT INTO `maincategory` (`id`, `name`) VALUES
(1, 'aaa'),
(2, 'bbb'),
(3, 'ggg');

-- --------------------------------------------------------

--
-- Table structure for table `maintosub`
--

CREATE TABLE `maintosub` (
  `main_id` int(11) NOT NULL,
  `sub_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `subcategory`
--

CREATE TABLE `subcategory` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `subcategory`
--

INSERT INTO `subcategory` (`id`, `name`) VALUES
(1, 'aaa'),
(2, 'bbb'),
(3, 'ccc'),
(4, 'fff'),
(5, 'eee'),
(6, 'bb'),
(7, 'ddd');

-- --------------------------------------------------------

--
-- Table structure for table `uploaded_by`
--

CREATE TABLE `uploaded_by` (
  `user_id` varchar(255) NOT NULL,
  `asset_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `uploaded_by`
--

INSERT INTO `uploaded_by` (`user_id`, `asset_id`) VALUES
('nahin', 2),
('nahin', 5),
('nahin', 6),
('nahin', 7),
('nahin', 8),
('nahin', 9);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `FName` text NOT NULL,
  `LName` text NOT NULL,
  `Email` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `Password`, `FName`, `LName`, `Email`) VALUES
('abc', '1111', 'aaa', 'bbb', 'aaa@gmail.com'),
('nahin', '123456', 'nahin', 'munkar', 'nahin@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `assets`
--
ALTER TABLE `assets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `asset_genre`
--
ALTER TABLE `asset_genre`
  ADD KEY `asset_genre_ibfk_1` (`asset_id`),
  ADD KEY `asset_genre_ibfk_2` (`genre_id`);

--
-- Indexes for table `asset_mainctg`
--
ALTER TABLE `asset_mainctg`
  ADD KEY `asset_mainctg_ibfk_1` (`asset_id`),
  ADD KEY `asset_mainctg_ibfk_2` (`main_id`);

--
-- Indexes for table `asset_subctg`
--
ALTER TABLE `asset_subctg`
  ADD KEY `asset_subctg_ibfk_1` (`asset_id`),
  ADD KEY `asset_subctg_ibfk_2` (`sub_id`);

--
-- Indexes for table `bookmark`
--
ALTER TABLE `bookmark`
  ADD KEY `user_id` (`user_id`),
  ADD KEY `asset_id` (`asset_id`);

--
-- Indexes for table `genre`
--
ALTER TABLE `genre`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `maincategory`
--
ALTER TABLE `maincategory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `maintosub`
--
ALTER TABLE `maintosub`
  ADD UNIQUE KEY `main_id` (`main_id`,`sub_id`),
  ADD KEY `maintosub_ibfk_2` (`sub_id`);

--
-- Indexes for table `subcategory`
--
ALTER TABLE `subcategory`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `uploaded_by`
--
ALTER TABLE `uploaded_by`
  ADD KEY `asset_id` (`asset_id`),
  ADD KEY `uploaded_by_ibfk_2` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `asset_genre`
--
ALTER TABLE `asset_genre`
  ADD CONSTRAINT `asset_genre_ibfk_1` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `asset_genre_ibfk_2` FOREIGN KEY (`genre_id`) REFERENCES `genre` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `asset_mainctg`
--
ALTER TABLE `asset_mainctg`
  ADD CONSTRAINT `asset_mainctg_ibfk_1` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `asset_mainctg_ibfk_2` FOREIGN KEY (`main_id`) REFERENCES `maincategory` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `asset_subctg`
--
ALTER TABLE `asset_subctg`
  ADD CONSTRAINT `asset_subctg_ibfk_1` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `asset_subctg_ibfk_2` FOREIGN KEY (`sub_id`) REFERENCES `subcategory` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `bookmark`
--
ALTER TABLE `bookmark`
  ADD CONSTRAINT `bookmark_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `bookmark_ibfk_2` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `maintosub`
--
ALTER TABLE `maintosub`
  ADD CONSTRAINT `maintosub_ibfk_1` FOREIGN KEY (`main_id`) REFERENCES `maincategory` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `maintosub_ibfk_2` FOREIGN KEY (`sub_id`) REFERENCES `subcategory` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `uploaded_by`
--
ALTER TABLE `uploaded_by`
  ADD CONSTRAINT `uploaded_by_ibfk_1` FOREIGN KEY (`asset_id`) REFERENCES `assets` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `uploaded_by_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
