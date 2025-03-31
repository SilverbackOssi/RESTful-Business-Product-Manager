from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle
from .models import Product
from .serializers import ProductSerializer

class CustomThrottle(AnonRateThrottle):
    def allow_request(self, request, view):
        allow = super().allow_request(request, view)
        
        # Add rate limit headers to response
        request.throttle_status = {
            'X-RateLimit-Limit': self.rate.split('/')[0],
            'X-RateLimit-Remaining': self.num_requests,
            'X-RateLimit-Reset': int(self.wait())
        }
        
        return allow

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing products.
    Supports Create, Read, Update, Delete operations with rate limiting.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    throttle_classes = [CustomThrottle]
    
    def get_success_data(self, data=None, message=None):
        """Helper method to format successful responses"""
        return {
            "status": "success",
            "code": 200,
            "message": message or "Operation completed successfully",
            "data": data
        }
    
    def get_error_data(self, status_code, message, details=None):
        """Helper method to format error responses"""
        return {
            "status": "error",
            "code": status_code,
            "message": message,
            "errors": {"details": details or message}
        }
    
    def list(self, request, *args, **kwargs):
        """Get all products with pagination"""
        paginator = PageNumberPagination()
        paginator.page_size = 10
        products = self.get_queryset()
        result_page = paginator.paginate_queryset(products, request)
        serializer = self.get_serializer(result_page, many=True)
        
        # Create pagination data
        pagination_data = {
            "current_page": paginator.page.number,
            "per_page": paginator.page_size,
            "total_pages": paginator.page.paginator.num_pages,
            "total_products": paginator.page.paginator.count
        }
        
        # Create links for navigation
        links = {
            "self": request.build_absolute_uri()
        }
        
        if paginator.get_next_link():
            links["next"] = paginator.get_next_link()
        else:
            links["next"] = None
            
        if paginator.get_previous_link():
            links["prev"] = paginator.get_previous_link()
        else:
            links["prev"] = None
        
        response_data = self.get_success_data(
            data={"products": serializer.data, "pagination": pagination_data},
            message="Products retrieved successfully"
        )
        
        response = Response(response_data)
        response.data["links"] = links
        
        # Add rate limit headers
        if hasattr(request, 'throttle_status'):
            for key, value in request.throttle_status.items():
                response[key] = value
        
        return response
    
    def retrieve(self, request, *args, **kwargs):
        """Get a specific product by ID"""
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            response_data = self.get_success_data(
                data={"product": serializer.data},
                message="Product details retrieved successfully"
            )
            
            response = Response(response_data)
            
            # Add rate limit headers
            if hasattr(request, 'throttle_status'):
                for key, value in request.throttle_status.items():
                    response[key] = value
            
            return response
        except Exception as e:
            return Response(
                self.get_error_data(404, "Product not found", "No product was found with the given ID."),
                status=status.HTTP_404_NOT_FOUND
            )
    
    def create(self, request, *args, **kwargs):
        """Create a new product"""
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            self.perform_create(serializer)
            response_data = self.get_success_data(
                data={"product": serializer.data},
                message="Product created successfully"
            )
            
            response = Response(response_data, status=status.HTTP_201_CREATED)
            
            # Add rate limit headers
            if hasattr(request, 'throttle_status'):
                for key, value in request.throttle_status.items():
                    response[key] = value
                    
            return response
        
        return Response(
            self.get_error_data(400, "Validation error", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def update(self, request, *args, **kwargs):
        """Update an existing product"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            response_data = self.get_success_data(
                data={"product": serializer.data},
                message="Product updated successfully"
            )
            
            response = Response(response_data)
            
            # Add rate limit headers
            if hasattr(request, 'throttle_status'):
                for key, value in request.throttle_status.items():
                    response[key] = value
                    
            return response
        
        return Response(
            self.get_error_data(400, "Validation error", serializer.errors),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def destroy(self, request, *args, **kwargs):
        """Delete a product"""
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            
            response_data = self.get_success_data(
                message="Product deleted successfully"
            )
            
            response = Response(response_data)
            
            # Add rate limit headers
            if hasattr(request, 'throttle_status'):
                for key, value in request.throttle_status.items():
                    response[key] = value
                    
            return response
        except Exception as e:
            return Response(
                self.get_error_data(404, "Product not found", "No product was found with the given ID."),
                status=status.HTTP_404_NOT_FOUND
            )
