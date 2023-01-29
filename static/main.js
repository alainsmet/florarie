function Increment(idInput, stocProd, totalPrice = false, totalPriceClass = 'final-price') {
	var inputTarget = document.getElementById(idInput);
	var rawInputOld = Number(inputTarget.value);
	var rawInput = Math.min(Number(inputTarget.value) + 1,stocProd);
	inputTarget.value = rawInput;
	var cartButton = document.getElementById(idInput.replace('value-prod-','button-prod-'));
	if (cartButton) {
		var idProduct = idInput.replace('value-prod-','');
		idProduct = idProduct.replace('-promo','');
		cartButton.onclick = function() {window.location.href='/adauga_cos/' + idProduct + '/' + rawInput + '/';};
	}
	if (totalPrice == true){
		var classTarget = document.getElementsByClassName(totalPriceClass)[0];
		var totalPriceOld = classTarget.textContent.slice(2);
		totalPriceOld = totalPriceOld.replace(' lei', '');
		var basePrice = +(totalPriceOld) / rawInputOld;
		var totalPriceNew = basePrice * rawInput;
		classTarget.textContent = '= ' + totalPriceNew.toFixed(2) + ' lei';
	}
}

function Decrement(idInput, totalPrice = false, totalPriceClass = 'final-price') {
	var inputTarget = document.getElementById(idInput);
	var rawInput = Number(inputTarget.value);
	var rawInputOld = rawInput;
	if (rawInput == 0) {
		rawInput = 1;
	}
	rawInput = Math.max(rawInput - 1,1);
	inputTarget.value = rawInput;
	var cartButton = document.getElementById(idInput.replace('value-prod-','button-prod-'));
	if (cartButton) {
		var idProduct = idInput.replace('value-prod-','');
		idProduct = idProduct.replace('-promo','');
		cartButton.onclick = function() {window.location.href='/adauga_cos/' + idProduct + '/' + rawInput + '/';};
	}
	if (totalPrice == true){
		var classTarget = document.getElementsByClassName(totalPriceClass)[0];
		var totalPriceOld = classTarget.textContent.slice(2);
		totalPriceOld = totalPriceOld.replace(' lei', '');
		var basePrice = +(totalPriceOld) / rawInputOld;
		var totalPriceNew = basePrice * rawInput;
		classTarget.textContent = '= ' + totalPriceNew.toFixed(2) + ' lei';
	}
}

function Check(e) {
    var keyCode = (e.keyCode ? e.keyCode : e.which);
    if ((keyCode <= 47 || (keyCode >= 58 && keyCode <= 95) || keyCode >= 106) && keyCode != 13 && keyCode != 8 && keyCode != 27) {
        e.preventDefault();
    }
}

function CheckValue(textInput, stocProd, unitPrice, totalPrice = false, totalPriceClass = 'final-price') {
	var rawInput = textInput.value;
	rawInput = Math.min(rawInput, stocProd);
	rawInput = Math.max(rawInput, 1);
	textInput.value = rawInput;
	var cartButton = document.getElementById(textInput.id.replace('value-prod-','button-prod-'));
	if (cartButton) {
		var idProduct = textInput.id.replace('value-prod-','');
		idProduct = idProduct.replace('-promo','');
		cartButton.onclick = function() {window.location.href='/adauga_cos/' + idProduct + '/' + rawInput + '/';};
	}
	if (totalPrice == true){
		var classTarget = document.getElementsByClassName(totalPriceClass)[0];
		var totalPriceNew = unitPrice * rawInput;
		classTarget.textContent = '= ' + totalPriceNew.toFixed(2) + ' lei';
	}
}