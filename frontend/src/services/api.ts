const API_BASE_URL = 'http://127.0.0.1:8000'

export interface Category {
  id: number
  name: string
  description: string | null
}

export interface Product {
  id: number
  sku: string
  name: string
  category_id: number | null
  unit: string
  cost_price: number | string
  selling_price: number | string
  current_stock: number
  reorder_level: number
}

export interface ProductCreate {
  sku: string
  name: string
  category_id: number | null
  unit: string
  cost_price: number
  selling_price: number
  reorder_level: number
}

async function handleResponse<T>(
  response: Response
): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => null)

    throw new Error(
      error?.detail || 'Something went wrong'
    )
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json()
}

export async function getProducts(): Promise<Product[]> {
  const response = await fetch(
    `${API_BASE_URL}/products`
  )

  return handleResponse<Product[]>(response)
}

export async function getCategories(): Promise<Category[]> {
  const response = await fetch(
    `${API_BASE_URL}/categories`
  )

  return handleResponse<Category[]>(response)
}

export async function createProduct(
  product: ProductCreate
): Promise<Product> {
  const response = await fetch(
    `${API_BASE_URL}/products`,
    {
      method: 'POST',

      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify(product),
    }
  )

  return handleResponse<Product>(response)
}

export interface StockMovement {
  id: number
  product_id: number
  movement_type: string
  quantity: number
  stock_after: number
  reference: string | null
  notes: string | null
  created_at: string
}

export interface StockMovementCreate {
  product_id: number
  quantity: number
  reference: string | null
  notes: string | null
}
export async function stockIn(
  data: StockMovementCreate
): Promise<StockMovement> {
  const response = await fetch(
    `${API_BASE_URL}/inventory/stock-in`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  )

  return handleResponse<StockMovement>(response)
}

export async function stockOut(
  data: StockMovementCreate
): Promise<StockMovement> {
  const response = await fetch(
    `${API_BASE_URL}/inventory/stock-out`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  )

  return handleResponse<StockMovement>(response)
}

export async function getStockMovements():
  Promise<StockMovement[]> {
  const response = await fetch(
    `${API_BASE_URL}/inventory/movements`
  )

  return handleResponse<StockMovement[]>(response)
}

export interface Supplier {
  id: number
  name: string
  contact_person: string | null
  phone: string | null
  email: string | null
  address: string | null
  notes: string | null
  created_at: string
}

export interface SupplierCreate {
  name: string
  contact_person: string | null
  phone: string | null
  email: string | null
  address: string | null
  notes: string | null
}

export interface SupplierUpdate {
  name?: string
  contact_person?: string | null
  phone?: string | null
  email?: string | null
  address?: string | null
  notes?: string | null
}


export async function getSuppliers():
  Promise<Supplier[]> {
  const response = await fetch(
    `${API_BASE_URL}/suppliers`
  )

  return handleResponse<Supplier[]>(response)
}


export async function createSupplier(
  data: SupplierCreate
): Promise<Supplier> {
  const response = await fetch(
    `${API_BASE_URL}/suppliers`,
    {
      method: 'POST',

      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify(data),
    }
  )

  return handleResponse<Supplier>(response)
}


export async function updateSupplier(
  id: number,
  data: SupplierUpdate
): Promise<Supplier> {
  const response = await fetch(
    `${API_BASE_URL}/suppliers/${id}`,
    {
      method: 'PUT',

      headers: {
        'Content-Type': 'application/json',
      },

      body: JSON.stringify(data),
    }
  )

  return handleResponse<Supplier>(response)
}


export async function deleteSupplier(
  id: number
): Promise<void> {
  const response = await fetch(
    `${API_BASE_URL}/suppliers/${id}`,
    {
      method: 'DELETE',
    }
  )

  return handleResponse<void>(response)
}