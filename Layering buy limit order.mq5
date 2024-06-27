//+------------------------------------------------------------------+
//|                                     Layering buy limit order.mq5 |
//|                                                          BOON888 |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+

#property copyright "BOON888-2024"
#property link      "yapboonsiong888@gmail.com"
#property version   "1.0"
#property script_show_inputs

#include <Trade\Trade.mqh>

//create instance of the trade
CTrade trade;
CTrade c_trade;

//--- input parameters
enum ChooseOption {Target=1,NumOfPips=2};

input string   Option = "SELECT TargetPrice OR NumOfPips BELOW";
input string   NOTEWELL = "When TargetPrice is selected, Pips has no effect & Vice Versa";

input ChooseOption TargetOrPips = 2;
input int      Pips_4rm_AskPrice = 200; //Pips From Current Price(FirstLayer)
input double   TargetPrice = 0; //Target Price(FirstLayer)
input double   Lots = .01;
input double   TakeProfit = 0; // Take Profit
input double   StopLoss = 0; // Stop Loss
input int      NumOfBuyLimit = 1; //Number Of Layer
input int      PipsBetweenOrders = 50; //Pips Between Orders

//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
void OnStart()
  {
//---

   if (TerminalInfoInteger(TERMINAL_TRADE_ALLOWED))
     {
      int pick = MessageBox("You are about to open " + DoubleToString(NumOfBuyLimit, 0) + " Buylimit order(s)\n", "BuyLimit", 0x00000001);
      if (pick == 1)
      {
         double basePrice = WhereToBuy();
         for (int i = 0; i < NumOfBuyLimit; i++)
         {
            double orderPrice = basePrice - i * PipsBetweenOrders * _Point;
            place_order(orderPrice);
         }
      }

      // MODIFY SL AND TP OF BUY LIMIT ORDERS :
      for (int j = OrdersTotal() - 1; j >= 0; --j) {
         ulong ticket = OrderGetTicket(j);
         if (OrderGetString(ORDER_SYMBOL) == Symbol() && OrderGetInteger(ORDER_TYPE) == ORDER_TYPE_BUY_LIMIT) {
            c_trade.OrderModify(ticket, OrderGetDouble(ORDER_PRICE_OPEN), StopLoss, TakeProfit, ORDER_TIME_DAY, 0);
         }
      }

     }
   else
      MessageBox("Please enable AutoTrading");

  }
//+------------------------------------------------------------------+

double Ask = SymbolInfoDouble(_Symbol, SYMBOL_ASK);

//+------------------------------------------------------------------+
//|                                                                  |
//+------------------------------------------------------------------+
double WhereToBuy()
  {
   if (TargetOrPips == Target)
      return(TargetPrice);
   else
      return(Ask - Pips_4rm_AskPrice * _Point);
  }

//+------------------------------------------------------------------+
//|      Place order                                                 |
//+------------------------------------------------------------------+
void place_order(double price)
  {

   double stoplosslevel, takeprofitlevel;

   if (StopLoss == 0)
      stoplosslevel = 0;
   else
      stoplosslevel = StopLoss;  // Use actual price for SL

   if (TakeProfit == 0)
      takeprofitlevel = 0;
   else
      takeprofitlevel = TakeProfit;  // Use actual price for TP

   bool TBL = trade.BuyLimit(Lots, price, _Symbol, stoplosslevel, takeprofitlevel);

   if (TBL == false)
      Alert("OrderSend failed with error #", GetLastError());

  }
//+------------------------------------------------------------------+