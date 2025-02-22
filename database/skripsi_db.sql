-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 20, 2025 at 11:20 AM
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
-- Database: `skripsi_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `forms`
--

CREATE TABLE `forms` (
  `id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `status` smallint(6) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `forms`
--

INSERT INTO `forms` (`id`, `title`, `status`, `created_at`) VALUES
(1, 'Pertanyaan mendasar seputar teknologi', 1, '2025-02-11 08:19:17'),
(2, 'Survey Skill Kepribadian', 1, '2025-02-20 04:53:17');

-- --------------------------------------------------------

--
-- Table structure for table `form_answers`
--

CREATE TABLE `form_answers` (
  `id` int(11) NOT NULL,
  `form_id` int(11) NOT NULL,
  `question_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `answer_text` text NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `form_answers`
--

INSERT INTO `form_answers` (`id`, `form_id`, `question_id`, `user_id`, `answer_text`, `created_at`) VALUES
(31, 2, 5, 3, 'Poor', '2025-02-20 05:50:08'),
(32, 2, 6, 3, 'Average', '2025-02-20 05:50:08'),
(33, 2, 7, 3, 'Intermediate', '2025-02-20 05:50:08'),
(34, 2, 8, 3, 'Intermediate', '2025-02-20 05:50:08'),
(35, 2, 9, 3, 'Intermediate', '2025-02-20 05:50:08'),
(36, 2, 10, 3, 'Average', '2025-02-20 05:50:08');

-- --------------------------------------------------------

--
-- Table structure for table `form_questions`
--

CREATE TABLE `form_questions` (
  `id` int(11) NOT NULL,
  `form_id` int(11) NOT NULL,
  `question_text` text NOT NULL,
  `category` varchar(100) NOT NULL,
  `options` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL CHECK (json_valid(`options`)),
  `status` smallint(6) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `form_questions`
--

INSERT INTO `form_questions` (`id`, `form_id`, `question_text`, `category`, `options`, `status`, `created_at`) VALUES
(1, 1, 'Apakah anda menyukai pembahasan teknologi ?', 'text', '[]', 0, '2025-02-11 08:19:17'),
(2, 1, 'Bagaimana anda menanggapi kemajuan teknologi ?', 'text', '[]', 0, '2025-02-11 08:19:17'),
(3, 1, 'Sosial media yang anda gunakan saat ini ?', 'multiple_choice', '[\"Facebook\", \"Twitter\", \"Instagram\", \"Reddit\"]', 0, '2025-02-11 08:19:17'),
(4, 1, 'Apakah anda memiliki pengalaman dibidang teknologi ?', 'rating', '[\"Ya\", \"Tidak\"]', 0, '2025-02-11 08:19:17'),
(5, 2, 'Programming Skill', 'rating', '[\"Not Interested\", \"Poor\", \"Beginner\", \"Average\", \"Intermediate\", \"Excellent\", \"Professional\"]', 1, '2025-02-20 04:53:17'),
(6, 2, 'Database Fundamentals', 'rating', '[\"Not Interested \", \"Poor\", \"Beginner\", \"Average\", \"Intermediate\", \"Excellent\", \"Professional\"]', 1, '2025-02-20 04:53:17'),
(7, 2, 'Computer Architecture', 'rating', '[\"Not Interested \", \"Poor\", \"Beginner\", \"Average\", \"Intermediate\", \"Excellent\"]', 1, '2025-02-20 04:53:17'),
(8, 2, 'Cyber Security', 'rating', '[\"Not Interested\", \"Poor\", \"Beginner\", \"Average\", \"Intermediate\", \"Excellent\", \"Professional\"]', 1, '2025-02-20 04:53:17'),
(9, 2, 'Computer Networking', 'rating', '[\"Not Interested \", \"Poor\", \"Beginner\", \"Average\", \"Intermediate\", \"Excellent\", \"Professional\"]', 1, '2025-02-20 04:53:17'),
(10, 2, 'Project Management', 'rating', '[\"Not Interested\", \"Poor\", \"Beginner\", \"Average\", \"Intermediate\", \"Excellent\", \"Professional\"]', 1, '2025-02-20 04:53:17');

-- --------------------------------------------------------

--
-- Table structure for table `setting`
--

CREATE TABLE `setting` (
  `id` int(11) NOT NULL,
  `url` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `setting`
--

INSERT INTO `setting` (`id`, `url`) VALUES
(1, 'survey/2');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `nisn` bigint(50) DEFAULT NULL,
  `fullname` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `role` int(11) NOT NULL DEFAULT 99,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `nisn`, `fullname`, `email`, `date_of_birth`, `role`, `created_at`) VALUES
(2, 'aepsaefulloh', '$2b$12$Nw2iGj63SHI.7fp6knmBpO3OM9LPvCDCHkezLGkhrL3jWowbQFoeC', 1233211231, 'Aep Saefulloh', 'aepsaefulloh1396@gmail.com', '1996-04-03', 1, '2025-02-11 08:03:15'),
(3, 'guest', '$2b$12$DqhBIe/IlnPB9uxTaWS5Nu0rzs2xLZaTyKpJu1jdkaEozT5Qrkdku', 1231322221, 'Guest', 'guest@gmail.com', '2025-02-04', 99, '2025-02-11 08:14:28'),
(4, 'superadmin', '$2b$12$4kF9zfmpJC7jCxSmBIhklO82TddQDrdjYQsacu7wBso4zcnXKgbPu', 1113332254, 'Super Admin', 'superadmin@gmail.com', '2025-02-11', 1, '2025-02-11 08:15:11');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `forms`
--
ALTER TABLE `forms`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `form_answers`
--
ALTER TABLE `form_answers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `form_id` (`form_id`),
  ADD KEY `question_id` (`question_id`);

--
-- Indexes for table `form_questions`
--
ALTER TABLE `form_questions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `form_id` (`form_id`);

--
-- Indexes for table `setting`
--
ALTER TABLE `setting`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `forms`
--
ALTER TABLE `forms`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `form_answers`
--
ALTER TABLE `form_answers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `form_questions`
--
ALTER TABLE `form_questions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `setting`
--
ALTER TABLE `setting`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `form_answers`
--
ALTER TABLE `form_answers`
  ADD CONSTRAINT `form_answers_ibfk_1` FOREIGN KEY (`form_id`) REFERENCES `forms` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `form_answers_ibfk_2` FOREIGN KEY (`question_id`) REFERENCES `form_questions` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `form_questions`
--
ALTER TABLE `form_questions`
  ADD CONSTRAINT `form_questions_ibfk_1` FOREIGN KEY (`form_id`) REFERENCES `forms` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
