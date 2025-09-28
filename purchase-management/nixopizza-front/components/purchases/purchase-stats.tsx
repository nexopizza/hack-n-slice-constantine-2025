import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { getOrdersStats } from "@/lib/apis/purchase-list";
import { ShoppingCart, Clock, CheckCircle, DollarSign } from "lucide-react";
import { useEffect, useState } from "react";
import toast from "react-hot-toast";

export function PurchaseStats() {
  const [stats, setStats] = useState({
    pendingOrders: 0,
    confirmedOrders: 0,
    paidOrders: 0,
    totalValue: 0,
  });
  useEffect(() => {
    const fetchStats = async () => {
      const {
        pendingOrders,
        confirmedOrders,
        paidOrders,
        totalValue,
        success,
        message,
      } = await getOrdersStats();
      if (success) {
        setStats({ pendingOrders, confirmedOrders, paidOrders, totalValue });
      } else {
        toast.error(message || "Failed to fetch order stats");
      }
    };
    fetchStats();
  }, []);
  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Pending Orders</CardTitle>
          <Clock className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">{stats.pendingOrders}</div>
          <p className="text-xs text-muted-foreground">Awaiting processing</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">
            Confirmed Orders
          </CardTitle>
          <CheckCircle className="h-4 w-4 text-blue-600" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-blue-600">
            {stats.confirmedOrders}
          </div>
          <p className="text-xs text-muted-foreground">Ready for fulfillment</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Paid Orders</CardTitle>
          <p className="text-green-600">DZA</p>
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold text-green-600">
            {stats.paidOrders}
          </div>
          <p className="text-xs text-muted-foreground">Payment received</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium">Total Value</CardTitle>
          <ShoppingCart className="h-4 w-4 text-muted-foreground" />
        </CardHeader>
        <CardContent>
          <div className="text-2xl font-bold">
            {stats.totalValue.toFixed(2)} DA
          </div>
          <p className="text-xs text-muted-foreground">This month</p>
        </CardContent>
      </Card>
    </div>
  );
}
