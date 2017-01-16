
<HTML>
	<HEAD>
		<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<TITLE>Monitor Stock Delete</TITLE>
	</HEAD>
	
	<a href="monitor_select.html" target="_top"><img src="/image/home.ico" width="40" height="40"/></a><br>
<?php
	class Stock
	{
		public $id;
  	public $name;
  	public $price;
  	public $date;
  	public $type;
  	public $note;  
  	
  	public function getId()
  	{
  		return $this->id;	
  	}
	}
	
	function write_2_xml($xml_file, $stock_list)
	{
		$file = $xml_file;
		
		$newsXML = new SimpleXMLElement("<Stocks></Stocks>");
			
		foreach($stock_list as $stock)
		{
			echo 'Stock:'. $stock->name. '<br>';
			$newsStock = $newsXML->addChild('Stock');
			$newsStock->addAttribute('id',   $stock->id);
			$newsStock->addAttribute('name', $stock->name);
			$newsStock->addAttribute('price',$stock->price);
			$newsStock->addAttribute('date', $stock->date);
			$newsStock->addAttribute('type', $stock->type);
			$newsStock->addAttribute('note', $stock->note);
		}
		echo "Write XML File: ". $file;		
		$dom = new DOMDocument('1.0');
		$dom->preserveWhiteSpace = false;
		$dom->formatOutput = true;
		$dom->loadXML($newsXML->asXML());
    $dom->save($file);	    				
	}
?>

<?php
	echo "Delete Stock ID<br>";
	$stack_list =  array();
	$delet_id = $_POST ["stock_id"];	
	$myallsport = implode ("<br>", $delet_id);
	//echo $myallsport. "<br>";		      
	$monitor_xml_file = $_POST ["monitor_xml_file"];	
	$xml=simplexml_load_file($monitor_xml_file);
	foreach($xml->children() as $child)
  {  	  	
  	$id    = $child['id'];
  	$name  = $child['name'];
  	$price = $child['price'];
  	$date  = $child['date'];
  	$type  = $child['type'];
  	$note  = $child['note'];	
  	
  	if (!in_array($id, $delet_id))
  	{
  		//echo "Remain Stock Name:". $name. '<br>';
  		$stock = new Stock;
  		$stock->id    = $id; 
  		$stock->name  = $name;
  		$stock->price = $price; 
  		$stock->date  = $date; 
  		$stock->type  = $type; 
  		$stock->note  = $note; 
  		$stock_list[] = $stock;    			
  	}else{
  		echo 'Delete:'. $id. '<br>'; 	
  	}
  }  
  write_2_xml($monitor_xml_file, $stock_list);
?>

</HTML>