<?php
	$type = $_POST['type'];
	if($type == 0){
		$func = $_POST['func'];
		$params = $_POST['params'];
		$cmd = "python python/option.py $func $params";
		$response = shell_exec($cmd);
		echo $response;
	}else if($type == 1){
		$params = $_POST['params'];
		$cmd = "python python/search.py $params";
		$response = shell_exec($cmd);
		echo $response;
	}else{
		$params = $_POST['params'];
		$cmd = "python python/detail.py $params";
		$response = shell_exec($cmd);
		echo $response;
	}	
	
?>