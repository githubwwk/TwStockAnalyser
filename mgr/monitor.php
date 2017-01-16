<HEAD>    
	<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
</HEAD>
<BODY>
<a href="monitor_select.html" target="_top"><img src="/image/home.ico" width="40" height="40"/></a>
<Form Name ="monitor" Method ="POST" ACTION = "delete.php">
<?php
$monitor_xml_folder = 'cfg';
$monitor_type = $_POST ["monitor_type"];
if (empty($monitor_type))
{	
	$monitor_xml_file = './'. $monitor_xml_folder. '/monitor_longterm.xml';	
	echo '[Load Default]:';
}else{
	$monitor_xml_file = './'. $monitor_xml_folder. '/monitor_'. $monitor_type. '.xml'; 
	echo '[Monitor Type]:';
}

echo '<INPUT type="text" name="monitor_xml_file" value='. $monitor_xml_file. ' readonly>';
echo '<br><br>';

$xml=simplexml_load_file($monitor_xml_file);
 
  echo '<table width=\'400\'>';
	foreach($xml->children() as $child)
  {  	  	
  	$id    = $child['id'];
  	$name  = $child['name'];
  	$price = $child['price'];
  	$date  = $child['date'];
  	$type  = $child['type'];
  	$note  = $child['note'];
  	echo '<tr>';
  	echo '<td>'. "<INPUT type=CHECKBOX name=\"stock_id[]\" value=\"". $id ."\">". '</td>';
  	echo '<td>'. $id . '</td>' ;  	
  	echo '<td>'. $name . '</td>' ; 
  	echo '<td>'. $price . '</td>' ; 
  	echo '<td>'. $date . '</td>' ; 
  	echo '<td>'. $type . '</td>' ; 
  	echo '<td>'. $note . '</td>' ; 
  	echo '</tr>';
  } 
  echo '</table>';  
?>
	<INPUT TYPE=SUBMIT VALUE="Delete">
</Form>
<br>
<Form Name ="monitor" Method ="POST" ACTION = "add.php">
		<?php 		
	  echo '<INPUT type="text" name="monitor_xml_file" value='. $monitor_xml_file. ' readonly>'; 
	  ?>
		<table>
			<tr><td>*ID:</td><td><input type="text" name=id ></tr></td>
			<tr><td>*Name:</td><td> <input type="text" name=name ></tr></td>
			<tr><td>Price:</td><td><input type="text" name=price ></tr></td>
			<tr><td>Date:</td><td> <input type="text" name=date value="<?php echo date("Y/m/d"); ?>"> </tr></td>
			<!-- <tr><td>Type:</td><td> <input type="text" name=type ></tr></td> -->
			<tr><td>Type:</td><td> 
				<select name=type> 
					<option value="BUY">BUY</option>
  				<option value="SELL">SELL</option>
  				<option value="N/A">N/A</option>
  			</select>	
  		</tr></td>
			
			<tr><td>Note:</td><td> <input type="text" name=note ></tr></td>
		</table>
		<INPUT TYPE=SUBMIT VALUE="Add">
</Form>

