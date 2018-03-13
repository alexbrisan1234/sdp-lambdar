package helpers;


public interface Callback<C, T>
{
    public void accept(C class_object, T member);
}
