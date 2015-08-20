using TabletTopTablet;
using TableTopTablet.Common;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Diagnostics;
using Windows.Devices.Input;
using Windows.Foundation;
using Windows.Foundation.Collections;
using Windows.Storage;
using Windows.Storage.Streams;
using Windows.UI;
using Windows.UI.Core;
using Windows.UI.Input.Inking;
using Windows.UI.Popups;
using Windows.UI.Xaml;
using Windows.UI.Xaml.Controls;
using Windows.UI.Xaml.Controls.Primitives;
using Windows.UI.Xaml.Data;
using Windows.UI.Xaml.Input;
using Windows.UI.Xaml.Media;
using Windows.UI.Xaml.Navigation;
using Windows.UI.Xaml.Shapes;

// The Blank Page item template is documented at http://go.microsoft.com/fwlink/?LinkId=234238

namespace TabletTopTablet
{
    /// <summary>
    /// An empty page that can be used on its own or navigated to within a Frame.
    /// </summary>
    public sealed partial class ViewQuestionPage : Page
    {
        InkManager MyInkManager = new InkManager();
        string DrawingTool;
        double X1, X2, Y1, Y2, StrokeThickness = 1;
        Line NewLine;
        Ellipse NewEllipse;
        Point StartPoint, PreviousContactPoint, CurrentContactPoint;
        Polyline Pencil;
        Rectangle NewRectangle;
        Color BorderColor = Colors.Black, FillColor;
        uint PenID, TouchID;

        private TransformGroup _transformGroup;
        private MatrixTransform _previousTransform;
        private CompositeTransform _compositeTransform;

        public ViewQuestionPage()
        {
            this.InitializeComponent();
            InitManipulationTransforms();
            canvas.PointerMoved += canvas_PointerMoved;
            canvas.PointerReleased += canvas_PointerReleased;
            canvas.PointerPressed += canvas_PointerPressed;
            canvas.PointerExited += canvas_PointerExited;
            canvas.PointerEntered += canvas_PointerEntered;

            for (int i = 1; i < 21; i++)
            {
                ComboBoxItem Items = new ComboBoxItem();
                Items.Content = i;
                cbStrokeThickness.Items.Add(Items);
            }
            cbStrokeThickness.SelectedIndex = 0;

            //var t = typeof(Colors);
            //var ti = t.GetTypeInfo();
            //var dp = ti.DeclaredProperties;

            var colors = typeof(Colors).GetTypeInfo().DeclaredProperties;
            foreach (var item in colors)
            {
                cbBorderColor.Items.Add(item);
                cbFillColor.Items.Add(item);
            }
        }



        /// <summary>
        /// Invoked when this page is about to be displayed in a Frame.
        /// </summary>
        /// <param name="e">Event data that describes how this page was reached.  The Parameter
        /// property is typically used to configure the page.</param>
        protected override void OnNavigatedTo(NavigationEventArgs e)
        {
        }

        #region Pointer Events

        void canvas_PointerEntered(object sender, PointerRoutedEventArgs e)
        {
            if (DrawingTool == "Select")
                Window.Current.CoreWindow.PointerCursor = new CoreCursor(CoreCursorType.Arrow, 1);
        }

        void canvas_PointerExited(object sender, PointerRoutedEventArgs e)
        {
            Window.Current.CoreWindow.PointerCursor = new CoreCursor(CoreCursorType.Arrow, 1);
        }

        void canvas_PointerPressed(object sender, PointerRoutedEventArgs e)
        {
            if (DrawingTool != "Eraser" && DrawingTool != "Select")
                Window.Current.CoreWindow.PointerCursor = new CoreCursor(CoreCursorType.Cross, 1);
            else if (DrawingTool == "Select")
                Window.Current.CoreWindow.PointerCursor = new CoreCursor(CoreCursorType.Arrow, 1);
            else
                Window.Current.CoreWindow.PointerCursor = new CoreCursor(CoreCursorType.UniversalNo, 1);

            switch (DrawingTool)
            {
                case "Line":
                    {
                        NewLine = new Line();
                        NewLine.X1 = e.GetCurrentPoint(canvas).Position.X;
                        NewLine.Y1 = e.GetCurrentPoint(canvas).Position.Y;
                        NewLine.X2 = NewLine.X1 + 1;
                        NewLine.Y2 = NewLine.Y1 + 1;
                        NewLine.StrokeThickness = StrokeThickness;
                        NewLine.Stroke = new SolidColorBrush(BorderColor);
                        canvas.Children.Add(NewLine);
                    }
                    break;

                case "Pencil":
                    {
                        StartPoint = e.GetCurrentPoint(canvas).Position;
                        Pencil = new Polyline();
                        Pencil.Stroke = new SolidColorBrush(BorderColor);
                        Pencil.StrokeThickness = StrokeThickness;
                        canvas.Children.Add(Pencil);
                        /*
                        var MyDrawingAttributes = new InkDrawingAttributes();
                        MyDrawingAttributes.Size = new Size(StrokeThickness, StrokeThickness);
                        MyDrawingAttributes.Color = BorderColor;
                        MyDrawingAttributes.FitToCurve = true;
                        MyInkManager.SetDefaultDrawingAttributes(MyDrawingAttributes);

                        PreviousContactPoint = e.GetCurrentPoint(canvas).Position;
                        //PointerDeviceType pointerDevType = e.Pointer.PointerDeviceType;  to identify the pointer device
                        if (e.GetCurrentPoint(canvas).Properties.IsLeftButtonPressed)
                        {
                            // Pass the pointer information to the InkManager.
                            MyInkManager.ProcessPointerDown(e.GetCurrentPoint(canvas));
                            PenID = e.GetCurrentPoint(canvas).PointerId;
                            e.Handled = true;
                        }
                         * */
                    }
                    break;

                case "Rectagle":
                    {
                        NewRectangle = new Rectangle();
                        X1 = e.GetCurrentPoint(canvas).Position.X;
                        Y1 = e.GetCurrentPoint(canvas).Position.Y;
                        X2 = X1;
                        Y2 = Y1;
                        NewRectangle.Width = X2 - X1;
                        NewRectangle.Height = Y2 - Y1;
                        NewRectangle.StrokeThickness = StrokeThickness;
                        NewRectangle.Stroke = new SolidColorBrush(BorderColor);
                        NewRectangle.Fill = new SolidColorBrush(FillColor);
                        canvas.Children.Add(NewRectangle);
                        NewRectangle.ManipulationMode = ManipulationModes.All;
                        NewRectangle.RenderTransform = _transformGroup;
                        NewRectangle.ManipulationDelta += NewRectangle_ManipulationDelta;
                    }
                    break;

                case "Ellipse":
                    {
                        NewEllipse = new Ellipse();
                        X1 = e.GetCurrentPoint(canvas).Position.X;
                        Y1 = e.GetCurrentPoint(canvas).Position.Y;
                        X2 = X1;
                        Y2 = Y1;
                        NewEllipse.Width = X2 - X1;
                        NewEllipse.Height = Y2 - Y1;
                        NewEllipse.StrokeThickness = StrokeThickness;
                        NewEllipse.Stroke = new SolidColorBrush(BorderColor);
                        NewEllipse.Fill = new SolidColorBrush(FillColor);
                        canvas.Children.Add(NewEllipse);
                    }
                    break;

                case "Eraser":
                    {
                        Window.Current.CoreWindow.PointerCursor = new CoreCursor(CoreCursorType.UniversalNo, 1);
                        StartPoint = e.GetCurrentPoint(canvas).Position;
                        Pencil = new Polyline();
                        Pencil.Stroke = new SolidColorBrush(Colors.Wheat);
                        Pencil.StrokeThickness = 10;
                        canvas.Children.Add(Pencil);
                    }
                    break;

                default:
                    break;
            }
        }

        void canvas_PointerMoved(object sender, PointerRoutedEventArgs e)
        {
            if (DrawingTool != "Eraser" && DrawingTool != "Select")
                Window.Current.CoreWindow.PointerCursor = new CoreCursor(CoreCursorType.Cross, 1);
            else if (DrawingTool == "Select")
                Window.Current.CoreWindow.PointerCursor = new CoreCursor(CoreCursorType.Arrow, 1);
            else
                Window.Current.CoreWindow.PointerCursor = new CoreCursor(CoreCursorType.UniversalNo, 1);

            switch (DrawingTool)
            {
                case "Pencil":
                    {
                        if (e.GetCurrentPoint(canvas).Properties.IsLeftButtonPressed == true)
                        {
                            if (StartPoint != e.GetCurrentPoint(canvas).Position && e.GetCurrentPoint(canvas).Position != null && Pencil != null)
                            {
                                Pencil.Points.Add(e.GetCurrentPoint(canvas).Position);
                            }
                        }
                        /*
                        if (e.Pointer.PointerId == PenID || e.Pointer.PointerId == TouchID)
                        {
                            // Distance() is an application-defined function that tests
                            // whether the pointer has moved far enough to justify 
                            // drawing a new line.
                            CurrentContactPoint = e.GetCurrentPoint(canvas).Position;
                            X1 = PreviousContactPoint.X;
                            Y1 = PreviousContactPoint.Y;
                            X2 = CurrentContactPoint.X;
                            Y2 = CurrentContactPoint.Y;

                            if (Distance(X1, Y1, X2, Y2) > 2.0)
                            {
                                Line line = new Line()
                                {
                                    X1 = X1,
                                    Y1 = Y1,
                                    X2 = X2,
                                    Y2 = Y2,
                                    StrokeThickness = StrokeThickness,
                                    Stroke = new SolidColorBrush(BorderColor)
                                };

                                PreviousContactPoint = CurrentContactPoint;
                                canvas.Children.Add(line);
                                MyInkManager.ProcessPointerUpdate(e.GetCurrentPoint(canvas));
                            }
                        }
                         * */
                    }
                    break;

                case "Line":
                    {
                        if (e.GetCurrentPoint(canvas).Properties.IsLeftButtonPressed == true)
                        {
                            NewLine.X2 = e.GetCurrentPoint(canvas).Position.X;
                            NewLine.Y2 = e.GetCurrentPoint(canvas).Position.Y;
                        }
                    }
                    break;

                case "Rectagle":
                    {
                        if (e.GetCurrentPoint(canvas).Properties.IsLeftButtonPressed == true)
                        {
                            X2 = e.GetCurrentPoint(canvas).Position.X;
                            Y2 = e.GetCurrentPoint(canvas).Position.Y;
                            if ((X2 - X1) > 0 && (Y2 - Y1) > 0)
                                NewRectangle.Margin = new Thickness(X1, Y1, X2, Y2);
                            else if ((X2 - X1) < 0)
                                NewRectangle.Margin = new Thickness(X2, Y1, X1, Y2);
                            else if ((Y2 - Y1) < 0)
                                NewRectangle.Margin = new Thickness(X1, Y2, X2, Y1);
                            else if ((X2 - X1) < 0 && (Y2 - Y1) < 0)
                                NewRectangle.Margin = new Thickness(X2, Y1, X1, Y2);
                            NewRectangle.Width = Math.Abs(X2 - X1);
                            NewRectangle.Height = Math.Abs(Y2 - Y1);
                        }
                    }
                    break;

                case "Ellipse":
                    {
                        if (e.GetCurrentPoint(canvas).Properties.IsLeftButtonPressed == true)
                        {
                            X2 = e.GetCurrentPoint(canvas).Position.X;
                            Y2 = e.GetCurrentPoint(canvas).Position.Y;
                            if ((X2 - X1) > 0 && (Y2 - Y1) > 0)
                                NewEllipse.Margin = new Thickness(X1, Y1, X2, Y2);
                            else if ((X2 - X1) < 0)
                                NewEllipse.Margin = new Thickness(X2, Y1, X1, Y2);
                            else if ((Y2 - Y1) < 0)
                                NewEllipse.Margin = new Thickness(X1, Y2, X2, Y1);
                            else if ((X2 - X1) < 0 && (Y2 - Y1) < 0)
                                NewEllipse.Margin = new Thickness(X2, Y1, X1, Y2);
                            NewEllipse.Width = Math.Abs(X2 - X1);
                            NewEllipse.Height = Math.Abs(Y2 - Y1);
                        }
                    }
                    break;

                case "Eraser":
                    {
                        if (e.GetCurrentPoint(canvas).Properties.IsLeftButtonPressed == true)
                        {
                            if (StartPoint != e.GetCurrentPoint(canvas).Position)
                            {
                                Window.Current.CoreWindow.PointerCursor = new CoreCursor(CoreCursorType.UniversalNo, 1);
                                Pencil.Points.Add(e.GetCurrentPoint(canvas).Position);
                            }
                        }
                    }
                    break;

                default:
                    break;
            }
        }

        private double Distance(double x1, double y1, double x2, double y2)
        {
            double d = 0;
            d = Math.Sqrt(Math.Pow((x2 - x1), 2) + Math.Pow((y2 - y1), 2));
            return d;
        }

        void canvas_PointerReleased(object sender, PointerRoutedEventArgs e)
        {
            if (e.Pointer.PointerId == PenID || e.Pointer.PointerId == TouchID)
                MyInkManager.ProcessPointerUp(e.GetCurrentPoint(canvas));

            TouchID = 0;
            PenID = 0;
            e.Handled = true;
            Pencil = null;
            NewLine = null;
            NewRectangle = null;
            NewEllipse = null;
        }

        #endregion

        #region Drawing Tools Click Events

        private void btnPencil_Click(object sender, RoutedEventArgs e)
        {
            DrawingTool = "Pencil";
        }

        private void btnLine_Click(object sender, RoutedEventArgs e)
        {
            DrawingTool = "Line";
        }

        private void btnEllipse_Click(object sender, RoutedEventArgs e)
        {
            DrawingTool = "Ellipse";
        }

        private void btnRectagle_Click(object sender, RoutedEventArgs e)
        {
            DrawingTool = "Rectagle";
        }

        private void btnEraser_Click(object sender, RoutedEventArgs e)
        {
            DrawingTool = "Eraser";
        }

        private void btnClearScreen_Click(object sender, RoutedEventArgs e)
        {
            canvas.Children.Clear();
        }

        private void btnSelect_Click(object sender, RoutedEventArgs e)
        {
            DrawingTool = "Select";
        }

        #endregion

        #region Other events

        private void cbStrokeThickness_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            StrokeThickness = Convert.ToDouble(cbStrokeThickness.SelectedIndex + 1);
        }

        private void btnExit_Click(object sender, RoutedEventArgs e)
        {
            canvas.Children.Clear();
        }

        private void cbBorderColor_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (cbBorderColor.SelectedIndex != -1)
            {
                var pi = cbBorderColor.SelectedItem as PropertyInfo;
                BorderColor = (Color)pi.GetValue(null);
            }
        }

        private void cbFillColor_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (cbFillColor.SelectedIndex != -1)
            {
                var pi = cbFillColor.SelectedItem as PropertyInfo;
                FillColor = (Color)pi.GetValue(null);
            }
        }

        private async void btnSaveWritingAsImage_Click(object sender, RoutedEventArgs e)
        {
            if (MyInkManager.GetStrokes().Count > 0)
            {
                try
                {
                    Windows.Storage.Pickers.FileSavePicker SavePicker = new Windows.Storage.Pickers.FileSavePicker();
                    SavePicker.SuggestedStartLocation = Windows.Storage.Pickers.PickerLocationId.Desktop;
                    SavePicker.DefaultFileExtension = ".png";
                    SavePicker.FileTypeChoices.Add("PNG", new string[] { ".png" });
                    SavePicker.FileTypeChoices.Add("JPG", new string[] { ".jpg" });
                    StorageFile filesave = await SavePicker.PickSaveFileAsync();
                    IOutputStream ab = await filesave.OpenAsync(FileAccessMode.ReadWrite);
                    if (ab != null)
                        await MyInkManager.SaveAsync(ab);
                }

                catch (Exception)
                {
                    var MsgDlg = new MessageDialog("Only handwriting can be saved as image.", "Error while saving");
                    MsgDlg.ShowAsync();
                }
            }
            else
            {
                var MsgDlg = new MessageDialog("Only handwriting can be saved as image.", "Error while saving");
                await MsgDlg.ShowAsync();
            }
        }

        #endregion

        private void InitManipulationTransforms()
        {
            _transformGroup = new TransformGroup();
            _compositeTransform = new CompositeTransform();
            _previousTransform = new MatrixTransform() { Matrix = Matrix.Identity };

            _transformGroup.Children.Add(_previousTransform);
            _transformGroup.Children.Add(_compositeTransform);
        }

        void NewRectangle_ManipulationDelta(object sender, ManipulationDeltaRoutedEventArgs e)
        {
            //sender = new Rectangle();
            _previousTransform.Matrix = _transformGroup.Value;

            Point center = _previousTransform.TransformPoint(new Point(e.Position.X, e.Position.Y));
            _compositeTransform.CenterX = center.X;
            _compositeTransform.CenterY = center.Y;

            _compositeTransform.Rotation = e.Delta.Rotation;
            _compositeTransform.ScaleX = _compositeTransform.ScaleY = e.Delta.Scale;
            _compositeTransform.TranslateX = e.Delta.Translation.X;
            _compositeTransform.TranslateY = e.Delta.Translation.Y;

            e.Handled = true;
        }
    }
}