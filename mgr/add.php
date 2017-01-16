<HEAD>    
	<META http-equiv="Content-Type" content="text/html; charset=UTF-8">
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
	
	function write_2_xml($xml_file, $stock_list, $stock_new)
	{
		$file = $xml_file;
		//$date_str = date("ymdHis");
		//$file = $xml_file. '_'. $date_str. 'xml';
		
		$newsXML = new SimpleXMLElement("<Stocks></Stocks>");
	
		// Write Original
		foreach($stock_list as $stock)
		{
			//echo 'Stock:'. $stock->name. '<br>';
			$newsStock = $newsXML->addChild('Stock');
			$newsStock->addAttribute('id',   $stock->id);
			$newsStock->addAttribute('name', $stock->name);
			$newsStock->addAttribute('price',$stock->price);
			$newsStock->addAttribute('date', $stock->date);
			$newsStock->addAttribute('type', $stock->type);
			$newsStock->addAttribute('note', $stock->note);
		}
		
		// Write New
		$newsStock = $newsXML->addChild('Stock');
		$newsStock->addAttribute('id',   $stock_new->id);
		$newsStock->addAttribute('name', $stock_new->name);
		$newsStock->addAttribute('price',$stock_new->price);
		$newsStock->addAttribute('date', $stock_new->date);
		$newsStock->addAttribute('type', $stock_new->type);
		$newsStock->addAttribute('note', $stock_new->note);
		
		// Show New Stock Information
		echo "Add New Stock: <br>";
		echo "[id]:". $stock_new->id ."<br>";
		echo "[name]:". $stock_new->name ."<br>";
		echo "[price]:". $stock_new->price ."<br>";
		echo "[date]:". $stock_new->date ."<br>";
		echo "[type]:". $stock_new->type ."<br>";
		echo "[note]:". $stock_new->note ."<br>";
		
		echo '<br>';
		echo "[Write XML File]: ". $file;		
		$dom = new DOMDocument('1.0');
		$dom->preserveWhiteSpace = false;
		$dom->formatOutput = true;
		$dom->loadXML($newsXML->asXML());
    $dom->save($file);	
    //$current = $dom->saveXMl();
    //echo $current;
    //file_put_contents($file, $current);        				
    //$fh = fopen($file, 'w') or die(" can't open file");
	}
	
	function read_4_xml($xml_file)
	{
		$stock_list =  array();		 
		$xml=simplexml_load_file($xml_file);
		//echo "Read XML:".	$xml_file. '<br>';
		foreach($xml->children() as $child)
  	{  	  	
  		$id    = $child['id'];
  		$name  = $child['name'];
  		$price = $child['price'];
  		$date  = $child['date'];
  		$type  = $child['type'];
  		$note  = $child['note'];	
  	  		
  		$stock = new Stock;
  		$stock->id    = $id; 
  		$stock->name  = $name;
  		$stock->price = $price; 
  		$stock->date  = $date; 
  		$stock->type  = $type; 
  		$stock->note  = $note; 
  		$stock_list[] = $stock;    			
  		
  		//echo "id:". $stock->id. '<br>';
  	}//foreach  		
  	$xml = null;
  	return $stock_list;
	}
?>

<?php
  $monitor_xml_file = $_POST ["monitor_xml_file"];
	$id    = $_POST ["id"];
	$name  = $_POST ["name"];
	$price = $_POST ["price"];
	$type  = $_POST ["type"];
	$date  = $_POST ["date"];
	$note  = $_POST ["note"];	
	
	$stock = new Stock;
  $stock->id    = $id; 
  $stock->name  = $name;
  $stock->price = $price; 
  $stock->date  = $date; 
  $stock->type  = $type; 
  $stock->note  = $note;   		
  		
	$stock_list = read_4_xml($monitor_xml_file);	
	//echo sizeof($stock_list);
	write_2_xml($monitor_xml_file, $stock_list, $stock);	
?>